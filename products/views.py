import json
from math import ceil

from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.utils.text import slugify

from items.utils import add_views
from items.models import Brand
from .elastic_agent import ElasticSearchAgent
from .utils import send_email, ask_for_part, set_cookie, save_orders, reply_on_order, get_category_parts
from .categories import get_parts_by_categories

es = ElasticSearchAgent()


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
    brand = request.GET.get("brand", None)
    models = es.get_models(brand)
    models.sort()
    json_object = [{"model": model} for model in models]
    return JsonResponse(json_object, safe=False)


def show_model(request):
    model = request.GET.get("model")
    page = int(request.GET.get("page", 1))
    category = request.GET.get("category", "none")
    if page > 1000:
        return redirect(reverse("show_model") + f"?model={model}")
    page_num = page - 1
    per_page = 10
    _from = page_num * per_page
    if category == "none":
        articles, total = es.show_model(model, _from)
    else:
        parts_by_category = get_parts_by_categories(category)
        articles = []
        for category_part in parts_by_category:  # Getting parts based on a chosen category.
            parts = get_category_parts(category_part, model)
            articles.extend(parts if parts else [])
        articles = [obj for obj in articles if obj]
        total = len(articles)
        articles = articles[(10*page-10): (10*page)]
        if not articles:
            return render(request, "model-parts-list.html", {"category": category, "model": model})
    on_page = min(total - _from, 10)
    total_num_pages = ceil(total / 10)
    if page > total_num_pages:
        return redirect(reverse("show_model") + f"?model={model}")
    context = {
        "model": model,
        "articles": articles,
        "page": page,
        "total": total_num_pages,
        "total_parts": total,
        "on_page": on_page,
        "category_search": category
    }
    return render(request, "model-parts-list.html", context)


def order(request):
    if request.method != "POST":
        return redirect(reverse("index"))
    payload = request.body.decode("utf-8")
    body = json.loads(payload)
    products = body["products"]
    if not products:
        return JsonResponse({})
    save_orders(products)
    response = send_email(body)
    print(response)
    if response["success"]:
        reply_on_order(body)
    return JsonResponse(response)


def show_models(request, brand):
    models = es.get_models(brand)
    brand_model_ids = [Brand.objects.filter(name=model).first() for model in models]
    models.sort()
    return render(request, "models.html", context={"models": models, "brand": brand, "brand_models": brand_model_ids})


def dynamic_search(request):
    searched_item = request.GET.get("search")
    parts, total = es.fine_tune_search(searched_item)
    return render(request, "dynamic-search.html", context={"products": parts})


def search_parts(request):
    if request.GET.get("checkbox"):
        model = request.GET.get("myModel")
    elif request.GET.get("modelSearch"):
        model = request.GET.get("modelSearch")
    else:
        model = None
    part = request.GET.get("search")
    page = int(request.GET.get("page", 1))
    if page > 1000:
        return redirect(reverse("index"))
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


def search_on_mobile(request):
    search_type = request.GET.get("searchRadioGroup")
    if search_type == "oem":
        oem = request.GET.get("search")
        article = es.search_product_by_oem(oem)
        if not article:
            return render(request, "unknown-search.html", context={"oem_number": "unknown"})
        gbg_id = article.get("gbg_id")
        return redirect("item:product_details", gbg_id)
    elif search_type == "kat":
        gbg_id = request.GET.get("search")
        article = es.get_product(gbg_id)
        return redirect("item:product_details", gbg_id) if article else render(request, "unknown-search.html")
    else:
        part = request.GET.get("search")
        _from = 0
        parts, total = es.search_part_query(part, _from)
        on_page = min(total - _from, 10)
        total_num_pages = ceil(total / 10)
        context = {
            "articles": parts,
            "page": 0,
            "total_parts": total,
            "total": total_num_pages,
            "on_page": on_page,
            "part": part,
            "model": None
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
    print(request.COOKIES)
    response = HttpResponse("")
    response.delete_cookie("my_brand")
    response.delete_cookie("my_model")
    return response


def add_to_cart(request, product_id):
    article = es.get_product(product_id)
    return render(request, "cart-scratch.html", context={"adding": True, "article": article})


def remove_from_cart(request):
    return render(request, "cart-scratch.html")


def quick_view(request, product_id):
    article = es.get_product(product_id)
    item = add_views(product_id)
    return render(request, "product-scratch.html", context={"item": item, "article": article})
