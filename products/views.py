import json
from Autodelovi.settings import CSRF_TRUSTED_ORIGINS

from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse

from .elastic_agent import ElasticSearchAgent
from .utils import send_email

es = ElasticSearchAgent()


def index(request):
    sijalice = es.sijalice_query()
    hladnjaci = es.hladnjaci_query()
    return render(request, 'home.html', context={'sijalice': sijalice, 'hladnjaci': hladnjaci})


def get_models(request):
    brand = request.GET.get('brand', None)
    models = es.get_models(brand)
    jason = [{'model': model} for model in models]
    return JsonResponse(jason, safe=False)


def show_model(request):
    query_param = request.GET.get('model')
    model = query_param.removesuffix('Izaberi model')
    page = request.GET.get('page')
    if not page:
        page = 1
        _from = 0
    else:
        page = int(page)
        per_page = 10
        _from = page * per_page

    articles = es.show_model(model, _from)
    context = {'model': model, 'articles': articles, 'page': page}
    return render(request, 'model-parts-list.html', context)


def product_details(request, product_id):
    article = es.get_product(product_id)
    context = {'article': article}
    return render(request, 'product.html', context)


def check_out(request):
    return render(request, 'checkout.html')


def order(request):
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        body = json.loads(payload)
        r = send_email(body)
        return JsonResponse(r.json())

    return JsonResponse(r.json())


def about(request):
    return render(request, 'onama.html')


def check_availability(request, product_id):
    if request.method == 'POST':
        telephone = request.POST.get("telephone")
        link = request.build_absolute_uri(reverse("product_details", args=[product_id]))
        # Ubaci slanje mejla.
        return redirect('index')
    return render(request, 'check-availability.html')


