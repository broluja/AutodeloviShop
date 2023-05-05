from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")


def brands(request):
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
    r = es.search(
        index="test-index",
        body=body
    )
    brands_raw = r["aggregations"]["models"]["buckets"][6:]
    b = [brand["key"] for brand in brands_raw]
    return {"brands": b}


def my_car(request):
    my_model = request.COOKIES.get("my_model")
    my_brand = request.COOKIES.get("my_brand")
    if all([my_model, my_brand]):
        return {"my_car": {"my_brand": my_brand, "my_model": my_model}}
    return {"my_car": None}
