from elasticsearch import Elasticsearch
from blog.models import Post

es = Elasticsearch("http://localhost:9200")


def brands(_request):
    body = {
        "_source": ["brand"],
        "size": 0,
        "aggs": {
            "models": {
                "terms": {
                    "field": "brand.keyword",
                    "size": 1000,
                    "order": {
                        "_key": "asc"
                    }

                }
            }
        }
    }
    r = es.search(index="test-index", body=body)
    brands_raw = r["aggregations"]["models"]["buckets"][5:]
    b = [brand["key"] for brand in brands_raw]
    return {"brands": b}


def my_car(request):
    my_model = request.COOKIES.get("my_model")
    my_brand = request.COOKIES.get("my_brand")
    if all([my_model, my_brand]):
        return {"my_car": {"my_brand": my_brand, "my_model": my_model}}
    return {"my_car": None}


def posts(_request):
    site_posts = Post.objects.all()
    return {"posts": site_posts}
