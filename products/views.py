import json
from math import ceil

from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse

from .elastic_agent import ElasticSearchAgent
from .utils import send_email, ask_for_part

es = ElasticSearchAgent()


def index(request):
    return render(request, 'home.html')


def check_for_part(request):
    item = request.GET.get("item")
    part = request.GET.get("part")
    if request.method != "POST":
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
    query_param = request.GET.get('model')
    model = query_param.removesuffix('Izaberi model')
    page = int(request.GET.get('page', 1))
    page_num = page - 1
    per_page = 10
    _from = page_num * per_page
    articles, total = es.show_model(model, _from)
    total_num_pages = ceil(total / 10)
    context = {'model': model, 'articles': articles, 'page': page, 'total': total_num_pages}
    if page > total_num_pages:
        raise Http404()
    return render(request, 'model-parts-list.html', context)


def product_details(request, product_id):
    article = es.get_product(product_id)
    context = {'article': article}
    return render(request, 'product.html', context)


def check_out(request):
    return render(request, 'checkout.html')


def order(request):
    if request.method == 'POST':
        print(request.POST)
        payload = request.body.decode('utf-8')
        body = json.loads(payload)
        r = send_email(body)
        return JsonResponse(r.json())

    return JsonResponse(r.json())


def about(request):
    return render(request, 'onama.html')


def open_model(request, model):
    models = es.get_models(model)
    models.sort()
    return render(request, "models.html", context={"models": models, "brand": model})
