from django.shortcuts import render
from products.elastic_agent import ElasticSearchAgent

from .models import Item

es = ElasticSearchAgent()


def product_details(request, product_id):
    article = es.get_product(product_id)
    item = Item.objects.filter(gbg_id=product_id).first()
    if not item:
        item = Item.objects.create(gbg_id=product_id)
    else:
        item.views += 1
        item.save()
    context = {'article': article, "item": item}
    return render(request, 'product.html', context)
