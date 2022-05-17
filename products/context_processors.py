from elasticsearch import Elasticsearch


es = Elasticsearch('http://localhost:9200')


body = {
        "_source": ["brand"],
        "size": 0,
        "aggs": {
            "models": {
                "terms": {
                    "field": "brand.keyword",
                    "size": 1000
                    , "order": {
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
brands_raw = r['aggregations']['models']['buckets'][6:]
b = [brand['key'] for brand in brands_raw]


def brands(request):
    return {'brands': b}
