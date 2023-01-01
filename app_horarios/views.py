from django.shortcuts import render

# Esto me dejará usar los formularios de Django de formularios.py
from .formularios import FormularioInicioSesion


# Create your views here.

""" Vista de la Página de Inicio.

"""
def index(request):
    return render(request, 'index.html')

""" Vista para la página de Iniciar Sesión.

Voy a incluir el formulario de Django para iniciar sesión.
"""
def iniciar_sesion(request):

    # Formulario de inicio de sesion
    formulario = FormularioInicioSesion

    return render(request, 'iniciar-sesion.html', {
        "formulario": formulario
    })
