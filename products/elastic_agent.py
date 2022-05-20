import requests
from elasticsearch import Elasticsearch

IMAGE_PATH = 'https://slike.digitalconstruct.rs'


class ElasticSearchAgent(object):

    def __new__(cls):
        print('Creating...')
        obj = super().__new__(cls)
        return obj

    def __init__(self):
        print('Instantiating...')
        self.port = 'http://localhost:9200'
        self.agent = Elasticsearch(self.port)

    def get_image(self, gbg_id):
        query = {
            "size": 1000,
            "query": {
                "match": {
                    "_id": gbg_id
                }
            }
        }
        r = self.agent.search(
            index="images",
            body=query
        )
        if not len(r['hits']['hits']):
            return None
        return r['hits']['hits']

    @staticmethod
    def image_exists(image_url):
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        if r.headers["content-type"] in image_formats:
            return True
        return False

    def img(self, gbg_id):
        model_id = str(gbg_id)[0:4]
        trd = self.get_image(gbg_id)
        file1 = f"{IMAGE_PATH}/{model_id}/{gbg_id}.jpg"
        file2 = f"{IMAGE_PATH}/{model_id}/{gbg_id}.JPG"
        first = self.image_exists(file1)
        second = self.image_exists(file2)
        third = None
        if trd is not None:
            third = str(trd[0])[0:4]

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
            image = self.img(gbg_id)
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
        for item in sijalice_raw:
            item = item['_source']
            gbg_id = item.get('gbg_id')
            image = self.img(gbg_id)
            item['image'] = image
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
        for item in hladnjaci_raw:
            item = item['_source']
            gbg_id = item.get('gbg_id')
            image = self.img(gbg_id)
            item['image'] = image
        hladnjaci = [item['_source'] for item in hladnjaci_raw]
        return hladnjaci

    def get_product(self, product_id):
        product_query = {
            "query": {
                "match": {
                    "gbg_id": product_id
                }
            }
        }
        p = self.agent.search(
            index='test-index',
            body=product_query
        )
        print('Product raw: ', p)
        product_dictionary = p['hits']['hits'][0]
        print('Product: ', product_dictionary)
        product = product_dictionary['_source']
        gbg_id = product['gbg_id']
        image = self.img(gbg_id)
        product['image'] = image
        print('Product Updated: ', product)
        return product
