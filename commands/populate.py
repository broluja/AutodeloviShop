import math
import csv23
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


es = Elasticsearch('http://localhost:9200')

output = "/home/autodelovi/ftp"
es.indices.delete(index='test-index')
es.index(index="test-index", document={})


def update_price(item_price):
    item_price = float(item_price)
    pdv = item_price * 0.2
    wholesale_cost = item_price + pdv

    if 0 <= wholesale_cost <= 500:
        new_price = wholesale_cost * 2

    elif 500 <= wholesale_cost <= 1000:
        new_price = wholesale_cost * 1.9

    elif 1000 <= wholesale_cost <= 2000:
        new_price = wholesale_cost * 1.6

    elif 2000 <= wholesale_cost <= 3000:
        new_price = wholesale_cost * 1.4

    elif 3000 <= wholesale_cost <= 4000:
        new_price = wholesale_cost * 1.3

    elif 4000 <= wholesale_cost <= 5000:
        new_price = wholesale_cost * 1.25

    elif 5000 <= wholesale_cost <= 7000:
        new_price = wholesale_cost * 1.2

    elif 7000 <= wholesale_cost <= 10000:
        new_price = wholesale_cost * 1.15

    elif 10000 <= wholesale_cost <= 13000:
        new_price = wholesale_cost * 1.12

    elif 13000 <= wholesale_cost <= 15000:
        new_price = wholesale_cost * 1.11

    else:
        new_price = wholesale_cost * 1.1

    final_pdv = new_price * 0.2
    final_price = new_price + final_pdv

    return math.ceil(final_price / 10) * 10


lista = []
file = f'{output}/PRICELIST_02850.txt'
with csv23.open_csv(file, encoding='iso-8859-1') as reader:
    for row in reader:
        data = row[0].split(';')
        gbg_id = ""
        genuine_code = ""
        description = ""
        side = ""
        model = ""
        price = ""
        weight = ""
        brand = ""

        try:
            resp = es.get(index="stock", id=data[0])
            stock = resp['_source']['stock']
        except Exception as exc:
            print(exc)
            stock = 0

        for i, field in enumerate(data):
            field = field.strip()
            if i == 0:
                gbg_id = field
            if i == 1:
                genuine_code = field
            if i == 2:
                description = field
            if i == 3:
                continue
            if i == 4:
                side = field
            if i == 5:
                model = field
            if i == 6:
                price = update_price(field)
            if i == 7:
                weight = field
            if i == 8:
                brand = field

        lista.append({
            "_index": "test-index",
            "_id": gbg_id,
            "_source": {
                'gbg_id': gbg_id,
                'genuine_code': genuine_code,
                'description': description,
                'side': side,
                'model': model,
                'price': price,
                'weight': weight,
                'brand': brand,
                'stock': stock
            }
        })

bulk(es, lista)
