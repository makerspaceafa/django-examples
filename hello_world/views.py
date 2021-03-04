from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

# Vai gerar uma HttpResponse, ou seja imprime o código html que estiver dentro
def index(request):
    return HttpResponse('Hello, world!')
    # return HttpResponse('<h1>Hello, world!</h1>')


# Como enviar conteúdo para o servidor -> através do url
def hello(request, name):
    # return HttpResponse(f"Hello, {name.capitalize()}!")

    # vai render um ficheiro html onde podemos por mais informação de forma organizada
    return render(request, 'hello_world/index.html', {
        'name': name
    })


# Podemos utilizar lógica python para desenvolver e processar os dados
def hello_day(request, name):
    day = datetime.today()
    return render(request, 'hello_world/day.html', {
        'name': name.capitalize(),
        'day': day.strftime('%d/%m/%Y')
    })
