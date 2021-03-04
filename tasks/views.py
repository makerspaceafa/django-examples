from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

# Create your views here.


class NewTaskForm(forms.Form):
    # tipos de fields -> Documentação -> Google it
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)


tasks = ['alpha', 'bravo', 'charlie']


def index(request):
    return render(request, 'tasks/index.html', {
        'tasks': tasks
    })


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            tasks.append(task)
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    else:
        return render(request, "tasks/add.html", {
            "form": NewTaskForm()
        })


# A lista criada até aqui está guardada numa variável global, ou seja,
# sempre que o website for inicialisado, independentemente do utilizador,
# vai aparecer a mesma lista.
# Para tornar a lista de tarefas pessoal, existe o conceito de sessions.
# mais detalhes em https://docs.djangoproject.com/en/3.1/topics/http/sessions/

# O código a seguir comentado representa o implementado acima mas com este
# novo conceito de sessions.

# def index(request):
#     if "tasks" not in request.session:
#         request.session["tasks"] = []
#     return render(request, "tasks/index.html", {
#         "tasks": request.session["tasks"]
#     })


# def add(request):
#     if request.method == "POST":
#         form = NewTaskForm(request.POST)
#         if form.is_valid():
#             task = form.cleaned_data["task"]
#             request.session["tasks"] += [task]
#             return HttpResponseRedirect(reverse("tasks:index"))
#         else:
#             return render(request, "tasks/add.html", {
#                 "form": form
#             })
#     else:
#         return render(request, "tasks/add.html", {
#             "form": NewTaskForm()
#         })
