"""
Definition of urls for polls viewing and voting.
"""


from . import views
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    # reference with {% url 'app:xxx %} , where xxx = name passed as last arg ↓↓
    path("", views.index, name='index'),
    path("register", views.index, name='kekw'),
    path("profile", views.index, name='profile'),
]
