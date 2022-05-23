import json

from Autodelovi.settings import MAIL_API_KEY, MAIL_SECRET_KEY, HOST_EMAIL
from mailjet_rest import Client
from tabulate import tabulate


def send_email(data):
    data["products"].insert(
        0,
        {'gbg_id': 'gbg_id', 'genuine_code': 'genuine_code', 'description': 'Naziv', 'side': 'Strana',
         'model': 'Model', 'price': "Cena", 'weight': 'Tezina', 'brand': 'Marka', 'stock': 'Stanje',
         'image': 'Slika', 'cart_count': "Kolicina"})
    products = tabulate(
        data["products"],
        tablefmt='html',
        headers="firstrow")
    html = f'{products} <br> TOTAL: {str(data["total"])} <br> Kupac: {json.dumps(data["user"])}'

    mailjet = Client(auth=(MAIL_API_KEY, MAIL_SECRET_KEY), version='v3.1')
    email = {
        'Messages': [
            {
                'From': {
                    'Email': "office@digitalconstruct.rs",
                    'Name': 'WebShop'
                },
                'To': [
                    {
                        'Email': 'stevan.meandzija@gmail.com',
                        'Name': "User"
                    }
                ],
                'Subject': "Porudzbina sa sajta",
                'TextPart': json.dumps(data["user"]),
                'HTMLPart': html
            }
        ]
    }
    r = mailjet.send.create(data=email)
    return r
