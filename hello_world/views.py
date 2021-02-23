from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

# Vai gerar uma HttpResponse, ou seja imprime o código html que estiver dentro
def index(request):
    return HttpResponse('Hello, world!')


# vai render um ficheiro html onde podemos por mais informação de forma organizada
def hello(request, name):
    # return HttpResponse(f"Hello, {name.capitalize()}!")
    return render(request, 'hello_world/index.html', {
        'name': name.capitalize()
    })


def hello_day(request, name):
    day = datetime.today()
    return render(request, 'hello_world/day.html', {
        'name': name.capitalize(),
        'day': day.strftime('%d/%m/%Y')
    })
