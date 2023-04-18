import json
from math import ceil

from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.utils.text import slugify

from .elastic_agent import ElasticSearchAgent
from .utils import send_email, ask_for_part, set_cookie, save_orders

es = ElasticSearchAgent()


def index(request):
    return render(request, 'home.html')


def check_for_part(request):
    if request.method != "POST":
        item = request.GET.get("item")
        part = request.GET.get("part")
        return render(request, "inquiry-form.html", context={"item": item, "part": part})
    model = request.POST.get("model-part")
    part_id = model.split("|")[1].strip()
    model = model.split("|")[0].strip()
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    text = request.POST.get("text")
    ask_for_part(model, part_id, phone, email, text)
    return HttpResponse(status=204)


def get_models(request):
    brand = request.GET.get('brand', None)
    models = es.get_models(brand)
    models.sort()
    jason = [{'model': model} for model in models]
    return JsonResponse(jason, safe=False)


def show_model(request):
    model = request.GET.get('model')
    page = int(request.GET.get('page', 1))
    page_num = page - 1
    per_page = 10
    _from = page_num * per_page
    articles, total = es.show_model(model, _from)
    total_num_pages = ceil(total / 10)
    context = {"model": model, "articles": articles, "page": page, "total": total_num_pages, "total_parts": total}
    if page > total_num_pages:
        return redirect(reverse('show_model') + f'?model={model}')
    return render(request, 'model-parts-list.html', context)


def check_out(request):
    return render(request, 'checkout.html')


def order(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        body = json.loads(payload)
        products = body["products"]
        save_orders(products)
        r = send_email(body)
        return JsonResponse(r.json())
    return redirect(reverse('index'))


def about(request):
    return render(request, 'onama.html')


def open_model(request, model):
    models = es.get_models(model)
    models.sort()
    return render(request, "models.html", context={"models": models, "brand": model})


def dynamic_search(request):
    searched_item = request.GET.get("search")
    parts, total = es.search_part_query(searched_item)
    return render(request, "dynamic-search.html", context={"products": parts})


def search_parts(request):
    if request.GET.get("checkbox"):
        model = request.GET.get("myModel")
    elif request.GET.get("modelSearch"):
        model = request.GET.get("modelSearch")
    else:
        model = None
    part = request.GET.get("search")
    page = int(request.GET.get('page', 1))
    page_num = page - 1
    per_page = 10
    _from = page_num * per_page
    parts, total = es.search_part_query(part, _from, model)
    on_page = min(total - _from, 10)
    total_num_pages = ceil(total / 10)
    context = {
        "articles": parts,
        "page": page,
        "total_parts": total,
        "total": total_num_pages,
        "on_page": on_page,
        "part": part,
        "model": model
    }
    return render(request, "search-parts-list.html", context)


def get_options(request):
    brand = request.GET.get("make", None)
    models = es.get_models(brand)
    models.sort()
    return render(request, "options-scratch.html", context={"models": models})


def add_car(request):
    brand = request.POST.get("make")
    model = request.POST.get("model")
    if brand == "Izaberi marku" or model == "Izaberi model":
        return HttpResponse("")
    slug = slugify(model)
    response = render(request, "car-icon-scratch.html", context={"model": model, "brand": brand, "slug": slug})
    set_cookie(response, "my_brand", brand, days_expire=365)
    set_cookie(response, "my_model", model, days_expire=365)
    return response


def clear(request):
    response = HttpResponse("")
    response.delete_cookie("my_brand")
    response.delete_cookie("my_model")
    return response
