import json
import datetime
from mailjet_rest import Client
from tabulate import tabulate

from django.http import Http404
from django.conf import settings

from items.models import Item
from Autodelovi.settings import MAIL_API_KEY, MAIL_SECRET_KEY


mailjet = Client(auth=(MAIL_API_KEY, MAIL_SECRET_KEY), version="v3.1")

def send_email(data):
    data["products"].insert(
        0,
        {"gbg_id": "gbg_id", "genuine_code": "genuine_code", "description": "Naziv", "side": "Strana",
         "model": "Model", "price": "Cena", "weight": "Tezina", "brand": "Marka", "stock": "Stanje",
         "image": "Slika", "cart_count": "Kolicina"})
    products = tabulate(
        data["products"],
        tablefmt='html',
        headers="firstrow")
    html = f"{products} <br> TOTAL: {str(data['total'])} <br> Kupac: {json.dumps(data['user'])}"

    email = {
        "Messages": [
            {
                "From": {
                    "Email": "office@digitalconstruct.rs",
                    "Name": "WebShop"
                },
                "To": [
                    {
                        "Email": "autodelovi011@gmail.com",
                        "Name": "User"
                    }
                ],
                "Subject": "Porudzbina sa sajta",
                "TextPart": json.dumps(data["user"]),
                "HTMLPart": html
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
    email = {
        "Messages": [
            {
                "From": {
                    "Email": "office@digitalconstruct.rs",
                    "Name": "WebShop"
                },
                "To": [
                    {
                        "Email": "autodelovi011@gmail.com",
                        "Name": "User"
                    }
                ],
                "Subject": "Porudzbina sa sajta",
                "HTMLPart": html
            }
        ]
    }
    return mailjet.send.create(data=email)

def send_questions(first_name, last_name, brand, model, part_description, part_id, genuine_code, question, phone, mail):
    html = f"<p>Molim Vas, imam pitanja u vezi dela</p>"
    html += f"<p>Brand: {brand} | Model: {model} | Part: {part_description} | ID: {part_id} | Genuine Code: {genuine_code}</p><br>"
    html += f"<section>{question}</section>"
    html += f"<p>Moj kontakt telefon: {phone}</p><p>Moj email: {mail}</p>"
    email = {
        "Messages": [
            {
                "From": {
                    "Email": "office@digitalconstruct.rs",
                    "Name": "WebShop"
                },
                "To": [
                    {
                        "Email": "olujic.branko@gmail.com",
                        "Name": "User"
                    }
                ],
                "Subject": f"Poruka od {first_name} {last_name}",
                "HTMLPart": html
            }
        ]
    }
    return mailjet.send.create(data=email)


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None
    )


def save_orders(products: list) -> None:
    try:
        for product in products:
            product_id = product["gbg_id"]
            quantity = product["cart_count"]
            item = Item.objects.filter(gbg_id=product_id).first()
            if not item:
                item = Item.objects.create(gbg_id=product_id)
                item.orders += int(quantity)
            else:
                item.orders += int(quantity)
            item.save()
    except Exception as exc:
        print(exc)
