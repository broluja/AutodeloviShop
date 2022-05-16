from django.shortcuts import render


def index(request):
    brands = []
    sijalice = []
    hladnjaci = []
    return render(request, 'home.html', context={'brands': brands, 'sijalice': sijalice, 'hladnjaci': hladnjaci})
