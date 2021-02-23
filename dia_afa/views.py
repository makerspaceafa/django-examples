from datetime import datetime

from django.shortcuts import render


# Create your views here.


def index(request):
    now = datetime.now()
    diaafa = now.month == 2 and now.day == 1
    return render(request, 'dia_afa/index.html', {
        'diaafa': diaafa
    })