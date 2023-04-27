from products.elastic_agent import ElasticSearchAgent
from items.models import Brand
from elasticsearch import Elasticsearch
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        es = Elasticsearch('http://localhost:9200')
        agent = ElasticSearchAgent()

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
        brands_raw = r['aggregations']['models']['buckets'][6:]
        brands = [brand['key'] for brand in brands_raw]
        for brand in brands:
            models = agent.get_models(brand)
            for model in models:
                part = agent.show_model(model, _from=0, per_page=1)
                Brand.objects.create(brand_id=part[0][0]["gbg_id"][:4], name=part[0][0]["model"])
        print("Brands are populated")
