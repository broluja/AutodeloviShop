from django.shortcuts import render

from products.utils import send_message


def index(request):
    """'Index' page."""
    return render(request, "home.html")


def about(request):
    """'About' page."""
    return render(request, "onama.html")


def contact(request):
    """Send email on 'Contact' page."""
    if request.method == "GET":
        return render(request, "contact.html")
    data = request.POST
    send_message(data)
    return render(request, "message-scratch.html")


def check_out(request):
    """'Checkout' page."""
    return render(request, "checkout.html")
