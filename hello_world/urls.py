from django.urls import path

# Create your urls here.
from hello_world import views

app_name = 'hello_world'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:name>', views.hello, name='hello'),
    path('<str:name>/day', views.hello_day, name='hello_day'),
]