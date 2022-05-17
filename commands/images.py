import csv23
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch('http://localhost:9200')
# es.indices.delete(index='images')
es.index(index="images", document={})

lista = []
file = '/home/branko/Documents/commands/ftp/REFAR_02850.txt'
with csv23.open_csv(file, encoding='iso-8859-1') as reader:
    for row in reader:
        data = row[0].split(';')
        lista.append({
            "_index": "images",
            "_id": data[0],
            "_source": {
                "image": data[1]
            }
        })

bulk(es, lista)

