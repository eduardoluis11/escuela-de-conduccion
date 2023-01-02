from django.shortcuts import render

# Esto me permitirá entrar a ciertas páginas de manera relativamente fácil
from django.http import HttpResponseRedirect

# Esto me permitirá regresar a la página de inicio de manera rápida
from django.urls import reverse

""" Esto me permitirá mostrar mensajes "flash", los cuales funcionarán como mensaje de confirmación. Además, para
abrir una nueva página, y poder mostrar el mensaje flash en esa página, usaré el "redirect".
"""
from django.contrib import messages
from django.shortcuts import redirect

# Este es el "decorator" que me permitirá mostrar cierto contenido solo a lus usuarios que hayan iniciado sesión
from django.contrib.auth.decorators import login_required

# Esto me permitirá iniciar y cerrar la sesión de un usuario
from django.contrib.auth import authenticate, login, logout



# Esto me dejará usar los formularios de Django de formularios.py
from .formularios import FormularioInicioSesion


# Create your views here.

""" Vista de la Página de Inicio.

"""
def index(request):
    return render(request, 'index.html')

""" Vista para la página de Iniciar Sesión.

Voy a incluir el formulario de Django para iniciar sesión.

Tengo que poner que, si se envía un POST request, que el usuario existente pueda iniciar sesión.
"""
def iniciar_sesion(request):

    # Formulario de inicio de sesion
    formulario = FormularioInicioSesion

    # Esto detectará si el usuario envió el formulario de inicio de sesión
    if request.method == "POST":

        # Esto agarra los datos escritos en los campos del formulario:
        nombre_de_usuario = request.POST["nombre_de_usuario"]
        contrasena = request.POST["contrasena"]

        # Esto chequeará si las credenciales existen en la base de datos
        usuario_existe = authenticate(request, username=nombre_de_usuario, password=contrasena)

        # Si el usuario existe, esto lo hará iniciar sesión
        if usuario_existe is not None:
            login(request, usuario_existe)
            return HttpResponseRedirect(reverse("index"))

        # Si el usuario no existe, esto mostrará un mensaje de error
        else:
            return render(request, "iniciar-sesion.html", {
                "mensaje": "Has escrito un nombre de usuario y/o contraseña incorrecta",
                "formulario": formulario
            })

    # Esto renderiza la página con el formulario
    else:
        return render(request, 'iniciar-sesion.html', {
            "formulario": formulario
        })

""" Vista para Cerrar la Sesión de un usuario.

Para activar esta vista, el usuario debe haber iniciado sesión. Por lo tanto, puse el decorator de que el usuario debió
haber iniciado sesión.
"""
@login_required
def cerrar_sesion(request):

    # Esto cierra la sesión del usuario
    logout(request)

    # Esto envía al usuario a la página de inicio
    return HttpResponseRedirect(reverse("index"))
