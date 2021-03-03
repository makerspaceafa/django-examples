from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

# Vai gerar uma HttpResponse, ou seja imprime o código html que estiver dentro
def index(request):
    return HttpResponse('Hello, world!')


# Como enviar conteúdo para o servidor -> através do url
def hello(request, name):
    # return HttpResponse(f"Hello, {name.capitalize()}!")

    # vai render um ficheiro html onde podemos por mais informação de forma organizada
    return render(request, 'hello_world/index.html', {
        'name': name.capitalize()
    })


def hello_day(request, name):
    day = datetime.today()
    return render(request, 'hello_world/day.html', {
        'name': name.capitalize(),
        'day': day.strftime('%d/%m/%Y')
    })
