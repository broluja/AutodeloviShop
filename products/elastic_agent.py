from elasticsearch import Elasticsearch

from .utils import img


class ElasticSearchAgent(object):

    def __new__(cls):
        print('Creating...')
        obj = super().__new__(cls)
        return obj

    def __init__(self):
        print('Instantiating...')
        self.port = 'http://localhost:9200'
        self.agent = Elasticsearch(self.port)

    def get_models(self, brand):
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
        r = self.agent.search(
            index="test-index",
            body=query
        )
        results = r['aggregations']['models']['buckets']
        models = [model['key'] for model in results]
        return models

    def show_model(self, model, _from, per_page=10):
        parts = {
            "from": _from,
            "size": per_page,
            "query": {
                "match": {
                    "model": model
                }
            }
        }
        s = self.agent.search(index='test-index',
                              body=parts)
        items = s['hits']['hits']

        for x in items:
            jsn = x['_source']
            gbg_id = jsn.get('gbg_id')
            image = img(gbg_id)
            jsn['image'] = image
        articles = [item['_source'] for item in items]
        return articles

    def sijalice_query(self):
        sijalice_query = {
            "size": 10,
            "query": {
                "match": {
                    "description": "sijalica"
                }
            }
        }
        s = self.agent.search(
            index='test-index',
            body=sijalice_query
        )
        sijalice_raw = s['hits']['hits']
        sijalice = [item['_source'] for item in sijalice_raw]
        return sijalice

    def hladnjaci_query(self):
        hladnjaci_query = {
            "size": 10,
            "query": {
                "match": {
                    "description": "hladnjak"
                }
            }
        }
        h = self.agent.search(
            index='test-index',
            body=hladnjaci_query
        )

        hladnjaci_raw = h['hits']['hits']
        hladnjaci = [item['_source'] for item in hladnjaci_raw]
        return hladnjaci
