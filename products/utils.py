import elasticsearch
import requests


es = elasticsearch.Elasticsearch('http://localhost:9200')


IMAGE_PATH = 'https://slike.digitalconstruct.rs'


def get_image(gbg_id):
    query = {
        "size": 1000,
        "query": {
            "match": {
                "_id": gbg_id
            }
        }
    }
    r = es.search(
        index="images",
        body=query
    )
    if not len(r['hits']['hits']):
        return None
    return r['hits']['hits']


def image_exists(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(image_url)
    if r.headers["content-type"] in image_formats:
        return True
    return False


def img(gbg_id):
    id = str(gbg_id)[0:4]
    trd = get_image(gbg_id)
    print(trd, 'AAAAAAAAAAAAAAAAAAA')
    file1 = f"{IMAGE_PATH}/{id}/{gbg_id}.jpg"
    file2 = f"{IMAGE_PATH}/{id}/{gbg_id}.JPG"
    first = image_exists(file1)
    second = image_exists(file2)
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
        _f1 = image_exists(f1)
        _f2 = image_exists(f2)
        if _f1:
            image = f1
        elif _f2:
            image = f2
        else:
            image = f"{IMAGE_PATH}/default.jpg"
    else:
        image = f"{IMAGE_PATH}/default.jpg"

    return image
