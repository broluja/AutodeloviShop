import requests
from elasticsearch import Elasticsearch

IMAGE_PATH = "https://slike.autodelovishop.rs/PARTS"


class ElasticSearchAgent:

    def __init__(self):
        self._port = "http://localhost:9200"
        self._agent = Elasticsearch(self.port)

    @property
    def port(self):
        return self._port

    @property
    def agent(self):
        return self._agent

    @staticmethod
    def image_exists(image_url: str) -> bool:
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        return r.headers["content-type"] in image_formats

    @staticmethod
    def get_parts_and_total(results: dict) -> tuple:
        total = results["hits"]["total"]["value"]
        parts = results["hits"]["hits"]
        return parts, total

    def get_image(self, gbg_id):
        query = {
            "size": 1000,
            "query": {
                "match": {"_id": gbg_id}
            }
        }
        r = self.agent.search(index="images", body=query)
        image = r["hits"]["hits"]
        return image if len(image) else None

    def img(self, gbg_id):
        model_id = str(gbg_id)[:4]
        trd = self.get_image(gbg_id)
        image_one = f"{IMAGE_PATH}/{model_id}/{gbg_id}.jpg"
        image_two = f"{IMAGE_PATH}/{model_id}/{gbg_id}.JPG"
        first = self.image_exists(image_one)
        second = self.image_exists(image_two)
        third = str(trd[0])[:4] if trd is not None else None
        if first:
            image = image_one
        elif second:
            image = image_two
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
        results = r["aggregations"]["models"]["buckets"]
        return [model["key"] for model in results]

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
        results = self.agent.search(index="test-index", body=parts)
        parts, total = self.get_parts_and_total(results)

        for x in parts:
            jsn = x["_source"]
            gbg_id = jsn.get("gbg_id")
            image = self.img(gbg_id)
            jsn["image"] = image
        return [item["_source"] for item in parts], total

    def search_part_query(self, part, from_=0, model=None, with_images=True):
        query = {
            "from": from_,
            "query": {
                "combined_fields": {
                    "query": part,
                    "fields": ["model^3", "description^2", "gbg_id", "genuine_code"]
                }
            }
        }
        if model:
            query["query"] = {
                "bool": {
                    "should": [{"bool": {"must": [
                        {
                            "fuzzy": {  # Tolerates slight errors in spelling.
                                "description": {"value": part.lower(), "fuzziness": "AUTO"}
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
        results = self.agent.search(index='test-index', body=query)
        parts, total = self.get_parts_and_total(results)
        if with_images:
            for item in parts:
                item = item["_source"]
                gbg_id = item.get("gbg_id")
                image = self.img(gbg_id)
                item["image"] = image
        return [item["_source"] for item in parts], total

    def get_product(self, product_id):
        product_query = {
            "query": {
                "match": {
                    "gbg_id": product_id
                }
            }
        }
        try:
            p = self.agent.search(index="test-index", body=product_query)
            product_dictionary = p["hits"]["hits"][0]
            product = product_dictionary["_source"]
            gbg_id = product["gbg_id"]
            image = self.img(gbg_id)
            product['image'] = image
            return product
        except IndexError as exc:
            print(exc)
            return []

    def get_products_twin(self, product, side):
        product_query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"model": product.get('model')}},
                        {"match": {"description": product.get('description')}},
                        {"match": {"side": side}},
                    ]
                }
            }
        }
        try:
            p = self.agent.search(index="test-index", body=product_query)
            product_dictionary = p["hits"]["hits"][0]
            product = product_dictionary["_source"]
            gbg_id = product["gbg_id"]
            image = self.img(gbg_id)
            product['image'] = image
            return product
        except IndexError as exc:
            print(exc)
            return None

    def search_product_by_oem(self, oem):
        product_query = {
            "query": {
                "match_phrase": {
                    "genuine_code": oem
                }
            }
        }
        p = self.agent.search(index="test-index", body=product_query)
        try:
            product_dictionary = p["hits"]["hits"][0]
            product = product_dictionary["_source"]
            gbg_id = product["gbg_id"]
            image = self.img(gbg_id)
            product['image'] = image
            return product
        except IndexError as exc:
            print(exc)
            return []

    def fine_tune_search(self, term: str):
        query = {
            "query": {
                "combined_fields": {
                    "query": term,
                    "fields": ["model^2", "description"]
                }
            }
        }
        results = self.agent.search(index="test-index", body=query)
        parts, total = self.get_parts_and_total(results)
        return [item["_source"] for item in parts], total

    def get_part_suggestion(self, term: str, model: str):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"model": model}},
                        {"match_phrase": {"description": {"query": term, "slop": 5}}}
                    ]  # Slop represents how far you're willing to let a term move to satisfy a phrase (both directions)
                }
            }
        }
        result = self.agent.search(index="test-index", body=query)
        if result.get("hits").get("hits"):
            part = result["hits"]["hits"][0]["_source"]
            gbg_id = part.get("gbg_id")
            image = self.img(gbg_id)
            part["image"] = image
            return part


    def get_parts_by_category(self, term: str, model: str):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"model": model}},
                        # {"match_phrase": {"description": {"query": term, "slop": 10}}},
                        {"fuzzy": {"description": {"value": term.lower(), "fuzziness": "AUTO"}}}
                    ]
                }
            }
        }

        result = self.agent.search(index="test-index", body=query)
        if result.get("hits").get("hits"):
            parts, total = self.get_parts_and_total(result)
            for item in parts:
                item = item["_source"]
                gbg_id = item.get("gbg_id")
                image = self.img(gbg_id)
                item["image"] = image
            return [item["_source"] for item in parts]
