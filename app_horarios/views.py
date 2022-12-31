from django.shortcuts import render

# Create your views here.

""" Vista de la Página de Inicio.

"""

def index(request):
    return render(request, 'index.html')
