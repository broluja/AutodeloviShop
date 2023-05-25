from django.shortcuts import render


def index(request):
    return render(request, "home.html")


def about(request):
    return render(request, "onama.html")


def check_out(request):
    return render(request, "checkout.html")
