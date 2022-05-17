from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.http import JsonResponse

from .utils import img


es = Elasticsearch('http://localhost:9200')


def index(request):
    sijalice_query = {
        "size": 10,
        "query": {
            "match": {
                "description": "sijalica"
            }
        }
    }
    s = es.search(
        index='test-index',
        body=sijalice_query
    )
    sijalice_raw = s['hits']['hits']
    sijalice = [item['_source'] for item in sijalice_raw]

    hladnjaci_query = {
        "size": 10,
        "query": {
            "match": {
                "description": "hladnjak"
            }
        }
    }
    h = es.search(
        index='test-index',
        body=sijalice_query
    )

    hladnjaci_raw = s['hits']['hits']
    hladnjaci = [item['_source'] for item in hladnjaci_raw]
    return render(request, 'home.html', context={'sijalice': sijalice, 'hladnjaci': hladnjaci})


def get_models(request):
    brand = request.GET.get('brand', None)
    query = {
        "_source": ["model"],
        "query": {
            "match": {
                "brand": brand
            }
        },
        "size": 0,
        "aggs": {
            "models": {
                "terms": {
                    "field": "model.keyword",
                    "size": 1000

                }
            }
        }
    }
    r = es.search(
        index="test-index",
        body=query
    )
    results = r['aggregations']['models']['buckets']
    models = [model['key'] for model in results]
    json = [{'model': model} for model in models]
    return JsonResponse(json, safe=False)


def show_model(request):
    query_param = request.GET.get('model')
    model = query_param.removesuffix('Izaberi model')
    per_page = 10
    page = request.GET.get('page')
    if not page:
        page = 1
        _from = 0
    else:
        page = int(page)
        _from = page * per_page
    parts = {
        "from": _from,
        "size": per_page,
        "query": {
            "match": {
                "model": model
            }
        }
    }
    s = es.search(index='test-index',
                  body=parts)
    items = s['hits']['hits']
    print(items)
    for x in items:
        jsn = x['_source']
        gbg_id = jsn.get('gbg_id')
        image = img(gbg_id)
        jsn['image'] = image
    articles = [item['_source'] for item in items]
    context = {'model': model, 'articles': articles, 'page': page}
    return render(request, 'model-parts-list.html', context)
