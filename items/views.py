from django.shortcuts import render
from django.http import HttpResponse

from products.elastic_agent import ElasticSearchAgent
from products.utils import send_questions
from .utils import add_views, get_group_of_connected_parts

es = ElasticSearchAgent()


def product_details(request, product_id):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("user_email")
        phone_prefix = request.POST.get("phone_country")
        phone_body = request.POST.get("phone_body")
        phone = f"{phone_prefix} {phone_body}"
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        part_description = request.POST.get("part_description")
        gen_code = request.POST.get("genuine_code")
        gbg_id = request.POST.get("gbg_id")
        question = request.POST.get("question")
        send_questions(first_name, last_name, brand, model, part_description, gbg_id, gen_code, question, phone, email)
        return HttpResponse(status=204)
    else:
        article = es.get_product(product_id)
        if article.get('side') == "R":  # Getting first suggestion in part suggestions (oposite side part, if exists.)
            first_suggestion = es.get_products_twin(article, side="L")
        elif article.get('side') == "L":
            first_suggestion = es.get_products_twin(article, side="R")
        else:
            first_suggestion = None
        model = article.get("model")
        familiar_parts = get_group_of_connected_parts(article.get("description").lower())
        articles = []
        if first_suggestion:
            articles.append(first_suggestion)
        for part in familiar_parts:  # Getting suggestion parts based on a group of familiar parts.
            part = es.get_part_suggestion(part, model)
            articles.append(part)
        articles = [obj for obj in articles if obj if obj.get("gbg_id") != article.get("gbg_id")]
        message = f"Povezani delovi modela {model}"
        if not articles:  # If no suggestions found
            articles, total = es.show_model(model, _from=0, per_page=3)
            message = f"Drugi proizvodi modela {model}"
        item = add_views(product_id)
        context = {"article": article, "item": item, "articles": articles, "message": message}
        return render(request, "product.html", context)
