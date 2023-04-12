import json
from mailjet_rest import Client
from tabulate import tabulate

from Autodelovi.settings import MAIL_API_KEY, MAIL_SECRET_KEY


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
                        'Email': 'autodelovi011@gmail.com',
                        'Name': "User"
                    }
                ],
                'Subject': "Porudzbina sa sajta",
                'TextPart': json.dumps(data["user"]),
                'HTMLPart': html
            }
        ]
    }
    return mailjet.send.create(data=email)


def ask_for_part(model, part_id, phone, email_address=None, text=None):
    html = f"<p>Molim Vas, proverite mi ovaj deo na stanju</p><br><p>Model: {model} | ID: {part_id}</p><br><br>"
    if text:
        html += f"<p>{text}</p><br><br>"
    html += f"<p>Moj kontakt telefon: {phone}"
    if email_address:
        html += f"<p>Moja email adresa: {email_address}"
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
                        'Email': 'autodelovi011@gmail.com',
                        'Name': "User"
                    }
                ],
                'Subject': "Porudzbina sa sajta",
                'HTMLPart': html
            }
        ]
    }
    return mailjet.send.create(data=email)
