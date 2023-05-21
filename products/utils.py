import json
import datetime
from mailjet_rest import Client
from tabulate import tabulate

from django.http import Http404
from django.conf import settings

from items.models import Item
from products.email_template import prolog, content, final
from Autodelovi.settings import MAIL_API_KEY, MAIL_SECRET_KEY


mailjet = Client(auth=(MAIL_API_KEY, MAIL_SECRET_KEY), version="v3.1")

def send_email(data):
    if not data:
        return
    data["products"].insert(
        0,
        {"gbg_id": "gbg_id", "genuine_code": "genuine_code", "description": "Naziv", "side": "Strana",
         "model": "Model", "price": "Cena", "weight": "Tezina", "brand": "Marka", "stock": "Stanje",
         "image": "Slika", "cart_count": "Kolicina"})
    products = tabulate(
        data["products"],
        tablefmt="html",
        headers="firstrow")
    byer = data['user']
    html = f"{products} <br> TOTAL: {data['total']:.2f} RSD<br> Kupac: {byer.get('name')} {byer.get('surname')}"
    html += f"<br>Ulica {byer.get('street')} broj, {byer.get('number')}, {byer.get('city')} - {byer.get('postcode')}"
    html += f"<br>Email: {byer.get('email')}"
    html +=  f"<br>Telefon: {byer.get('phone')}"
    html += f"<br>Komentar: {byer.get('comment')}"

    email = {
        "Messages": [
            {
                "From": {
                    "Email": "office@digitalconstruct.rs",
                    "Name": "AutoDeloviShop"
                },
                "To": [
                    {
                        "Email": "olujic.branko@gmail.com",
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


def reply_on_order(order_data):
    if not order_data:
        return
    name = order_data["user"]["name"] + " " + order_data["user"]["surname"]
    user_email = order_data['user']["email"]
    products = order_data["products"][1:]
    product_names = [product["description"] for product in products]
    prices = [product["price"] for product in products]
    links = [product["image"] for product in products]
    quantities = [product["cart_count"] for product in products]
    total = order_data["total"]
    html = f"Zdravo {name}, <br>"
    html += prolog + "<br>"
    html += content + "<br>"
    html += "Poručili ste: <br>"
    for name, price, link, quantity in zip(product_names, prices, links, quantities):
        html += f"{name} - cena: {price}, količina {quantity} | {link} <br>"

    html += f"Konačna cena je: {total}<br>"
    html += final

    email = {
        "Messages": [
            {
                "From": {
                    "Email": "office@digitalconstruct.rs",
                    "Name": "AutoDeloviShop"
                },
                "To": [
                    {
                        "Email": user_email,
                        "Name": "User"
                    }
                ],
                "Subject": "AutoDeloviShop - Moja porudžbina",
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
                    "Name": "AutoDeloviShop"
                },
                "To": [
                    {
                        "Email": "autodelovishop.rs@gmail.com",
                        "Name": "User"
                    }
                ],
                "Subject": "Porudzbina sa sajta",
                "HTMLPart": html
            }
        ]
    }
    return mailjet.send.create(data=email)

def send_questions(first_name, last_name, brand, model, part_desc, part_id, gen_code, question, phone, mail):
    html = f"<p>Molim Vas, imam pitanja u vezi dela</p>"
    html += f"<p>Brand: {brand} | Model: {model} | Part: {part_desc} | ID: {part_id} | Gen. Code: {gen_code}</p><br>"
    html += f"<section>{question}</section>"
    html += f"<p>Moj kontakt telefon: {phone}</p><p>Moj email: {mail}</p>"
    email = {
        "Messages": [
            {
                "From": {
                    "Email": "office@digitalconstruct.rs",
                    "Name": "AutoDeloviShop"
                },
                "To": [
                    {
                        "Email": "autodelovishop.rs@gmail.com",
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
            item, created = Item.objects.get_or_create(gbg_id=product_id)
            item.orders += int(quantity)
            item.save()
    except Exception as exc:
        print(exc)
