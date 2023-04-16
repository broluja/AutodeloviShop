import csv23
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch('http://localhost:9200')
# es.indices.delete(index='stock')
es.index(index="stock", document={})

lista = []
file = '/home/autodelovi/ftp/OUTOFSTOCK_SRB.txt'
with csv23.open_csv(file, encoding='iso-8859-1') as reader:
    for row in reader:
        data = row[0].split(';')
        lista.append({
            "_index": "stock",
            "_id": data[0],
            "_source": {
                "stock": data[1]
            }
        })

bulk(es, lista)
