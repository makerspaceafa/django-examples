"""DjangoExamples URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from simple_weather import views as sw
from main_app import views as main
from dia_afa import views as afa

urlpatterns = [
    path('', main.index),
    # ONLY EDIT BELOW
    # You can enable admin if you want
    # path('admin/', admin.site.urls),

    # To add a simple url just remember to provide a name!
    # This name is what shows up on the landing page index.
    path('sw/', sw.index, name='simple_weather'),
    path('hw/', include('hello_world.urls', 'hello_world')),
    path('afa/', afa.index, name='dia_afa'),
    # To include a urls file, remember to provide an app name!
    # This name will show on the landing page index.
    # If you provide an instance namespace, that will show up instead.
    # path('some-app/', include(('some_app.urls', 'some_app'))
]
