import datetime
import json
import mailtrap as mt
import redis
from mailjet_rest import Client
from tabulate import tabulate

from django.conf import settings
from django.http import Http404

from Autodelovi.settings import MAILTRAP_TOKEN, MAILTRAP_MAIL
from items.models import Item
from products.email_template import prolog, content, final
from .elastic_agent import ElasticSearchAgent

AUTODELOVI_MAIL = "autodelovishop.rs@gmail.com"

es = ElasticSearchAgent()
client = mt.MailtrapClient(token=MAILTRAP_TOKEN)

def send_email(data):
    """Send email on product order."""
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
    subject = "Porudzbina sa sajta"
    text = json.dumps(byer)
    mail = make_mail(AUTODELOVI_MAIL, subject, html, text)
    return client.send(mail)


def reply_on_order(order_data):
    """Send email as order response."""
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
        html += f"{name} - cena: {price: .2f}, količina {quantity} | {link} <br>"

    html += f"Konačna cena je: {total: .2f}<br>"
    html += final
    subject = "AutoDeloviShop - Moja porudžbina"
    mail = make_mail(user_email, subject, html)
    return client.send(mail)


def ask_for_part(model, part_id, phone, email_address=None, text=None):
    """Send email on product query."""
    html = f"<p>Molim Vas, proverite mi ovaj deo na stanju</p><br><p>Model: {model} | ID: {part_id}</p><br><br>"
    if text:
        html += f"<p>{text}</p><br><br>"
    html += f"<p>Moj kontakt telefon: {phone}"
    if email_address:
        html += f"<p>Moja email adresa: {email_address}"
    subject = "Upit sa sajta"
    mail = make_mail(AUTODELOVI_MAIL, subject, html)
    return client.send(mail)

def send_questions(first_name, last_name, brand, model, part_desc, part_id, gen_code, question, phone, mail):
    """Send email on product questions."""
    html = f"<p>Molim Vas, imam pitanja u vezi dela</p>"
    html += f"<p>Brand: {brand} | Model: {model} | Part: {part_desc} | ID: {part_id} | Gen. Code: {gen_code}</p><br>"
    html += f"<section>{question}</section>"
    html += f"<p>Moj kontakt telefon: {phone}</p><p>Moj email: {mail}</p>"
    html += f"<p>Srdačan pozdrav, {first_name} {last_name}</p>"
    subject = "Upit sa sajta"
    mail = make_mail(AUTODELOVI_MAIL, subject, html)
    return client.send(mail)


def send_message(data: dict):
    """Send message from 'Contact' page."""
    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    html = "<p>Poštovani, </p><br>"
    html += f"{message}<br>"
    if email:
        html += f"Dostupan sam na email adresi: {email}"
    subj = f"Poruka sa sajta - {subject}"
    text = json.dumps(data["name"])
    mail = make_mail(AUTODELOVI_MAIL, subj, html, text)
    return client.send(mail)


def make_mail(to: str, subject:str, html: str, text: str = None, from_: str = MAILTRAP_MAIL):
    """Make email for sendinf through mailtrap server."""
    mail = mt.Mail(
        sender=mt.Address(email=from_, name="AutoDeloviShop"),
        to=[mt.Address(email=to)],
        subject=subject,
        text=text,
        html=html,
    )
    return mail


def set_cookie(response, key, value, days_expire=7):
    """Setting cookie on the response."""
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
    """Increment orders on the ordered item."""
    try:
        for product in products:
            product_id = product["gbg_id"]
            quantity = product["cart_count"]
            item, created = Item.objects.get_or_create(gbg_id=product_id)
            item.orders += int(quantity)
            item.save()
    except Exception as exc:
        print(exc)


def memoize(func):
    """Cache on redis results from func return results."""
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    expire = 60 * 60 * 24

    def wrapper(*args):
        key = '_'.join(args)
        if r.get(key):
            data = r.get(key)
            return json.loads(data)
        else:
            result = func(*args)
            data = json.dumps(result)
            r.set(key, data, ex=expire)
            return result

    return wrapper


@memoize
def get_category_parts(category_part, model):
    parts = es.get_parts_by_category(category_part, model)
    return parts
