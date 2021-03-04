from datetime import datetime

from django.shortcuts import render

# Create your views here.


# O exemplo anterior utilizamos funções já existentes nas bibliotecas do python,
# mas podemos criar tbm a nossa própria lógica.

def index(request):
    now = datetime.now()
    # como é que sabemos que estas funções existem? Documentação -> Google it
    # django views functions

    diaafa = now.month == 2 and now.day == 1

    return render(request, 'dia_afa/index.html', {
        'diaafa': diaafa
    })
