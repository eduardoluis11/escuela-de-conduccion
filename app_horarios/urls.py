""" El "urlpatterns" me permitirá acceder a cada template o pagina a través de las distintas URLs (fuente:
https://youtu.be/pRNhdI9PVmg) .

"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
