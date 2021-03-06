import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpRequest

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
    json = [{'model': model} for model in models]
    return JsonResponse(json, safe=False)


def show_model(request):
    query_param = request.GET.get('model')
    model = query_param.removesuffix('Izaberi model')
    page = request.GET.get('page')
    per_page = 10
    if not page:
        page = 1
        _from = 0
    else:
        page = int(page)
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
    global r
    if request.method == 'POST':
        payload = request.body.decode('utf-8')
        body = json.loads(payload)
        r = send_email(body)

    return JsonResponse(r.json())
