import requests
from elasticsearch import Elasticsearch

IMAGE_PATH = 'https://slike.autodelovishop.rs'


class ElasticSearchAgent:

    def __init__(self):
        self.port = 'http://localhost:9200'
        self.agent = Elasticsearch(self.port)

    def get_image(self, gbg_id):
        query = {
            "size": 1000,
            "query": {
                "match": {"_id": gbg_id}
            }
        }
        r = self.agent.search(index="images", body=query)
        image = r['hits']['hits']
        return image if len(image) else None

    @staticmethod
    def image_exists(image_url):
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        return r.headers["content-type"] in image_formats

    def img(self, gbg_id):
        model_id = str(gbg_id)[:4]
        trd = self.get_image(gbg_id)
        file1 = f"{IMAGE_PATH}/{model_id}/{gbg_id}.jpg"
        file2 = f"{IMAGE_PATH}/{model_id}/{gbg_id}.JPG"
        first = self.image_exists(file1)
        second = self.image_exists(file2)
        third = str(trd[0])[:4] if trd is not None else None
        if first:
            image = file1
        elif second:
            image = file2
        elif third:
            f1 = f"{IMAGE_PATH}/{third}.jpg"
            f2 = f"{IMAGE_PATH}/{third}.JPG"
            _f1 = self.image_exists(f1)
            _f2 = self.image_exists(f2)
            if _f1:
                image = f1
            elif _f2:
                image = f2
            else:
                image = f"{IMAGE_PATH}/default.jpg"
        else:
            image = f"{IMAGE_PATH}/default.jpg"

        return image

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
        r = self.agent.search(index="test-index", body=query)
        results = r['aggregations']['models']['buckets']
        return [model['key'] for model in results]

    def show_model(self, model, _from, per_page=10, strict=True):
        if not strict:
            model += ".*"
        parts = {
            "from": _from,
            "size": per_page,
            "query": {
                "match_phrase_prefix": {
                    "model": {
                        "query": model
                    }
                }
            }
        }
        s = self.agent.search(index='test-index', body=parts)
        items = s['hits']['hits']
        total = s['hits']['total']['value']

        for x in items:
            jsn = x['_source']
            gbg_id = jsn.get('gbg_id')
            image = self.img(gbg_id)
            jsn['image'] = image
        return [item['_source'] for item in items], total

    def search_part_query(self, part, from_=0, model=None):
        query = {
            "size": 10,
            "from": from_,
            "query": {
                "match": {
                    "description": part
                }
            }
        }
        if model:
            query["query"] = {
                "bool": {
                    "should": [{"bool": {"must": [
                        {
                            "match": {
                                "description": part
                            }
                        },
                        {
                            "match_phrase_prefix": {
                                "model": model
                            }}]
                    }
                    }]
                }
            }
        s = self.agent.search(index='test-index', body=query)
        parts = s['hits']['hits']
        total = s['hits']['total']['value']
        for item in parts:
            item = item['_source']
            gbg_id = item.get('gbg_id')
            image = self.img(gbg_id)
            item['image'] = image
        return [item['_source'] for item in parts], total

    def get_product(self, product_id):
        product_query = {
            "query": {
                "match": {
                    "gbg_id": product_id
                }
            }
        }
        p = self.agent.search(index='test-index', body=product_query)
        product_dictionary = p['hits']['hits'][0]
        product = product_dictionary['_source']
        gbg_id = product['gbg_id']
        image = self.img(gbg_id)
        product['image'] = image
        return product
