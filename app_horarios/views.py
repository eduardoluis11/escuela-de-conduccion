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


# Esto importará todos los modelos que he creado
from .models import User, Chofer, Secretario, Oficina, Asistencia, ReporteSemanal, Estudiante, HorariosLunes, \
    HorariosMartes, HorariosMiercoles, HorariosJueves, HorariosViernes, HorariosSabados, PeticionParaCambiarHorario

# Esto me dejará usar los formularios de Django de formularios.py
from .formularios import FormularioInicioSesion


# Create your views here.

""" Vista de la Página de Inicio.

Necesito los IDs de todos los usuarios de la tabla “Chofer”. Así, usando Jinja, voy a comparar la ID del usuario 
logueado con las ID de los choferes. Si son la misma ID, quiere decir que el usuario es un chofer. Por lo tanto, le 
mostraré la página de inicio para choferes. 

Necesito usar un Query Set para agarrar todas las IDs de la tabla Chofer. Por los momentos, no necesito crear un
"array" ni una lista.

La variable en la tabla Chofer que tiene la ID de usuario de ese chofer se llama “id_de_usuario_id”. Esa es la 
variable que me dice la ID de usuario de ese chofer, y me dice si el usuario logueado es un chofer.
"""
def index(request):

    # Esto almacenará la ID del usuario si se loguea
    id_del_usuario_logueado = ''

    # Esto cheque si el usuario está logueado
    if request.user.is_authenticated:

        # Esto almacena la ID del usuario logueado como un integer
        id_del_usuario_logueado = int(request.user.id)

        # MENSAJE DE DEBUGGEO
        # print("Esta es la ID del usuario logueado:")
        # print(id_del_usuario_logueado)


    # Esto agarra las IDs de todos los choferes
    lista_de_choferes = Chofer.objects.all()

    # Bucle de DEBUGGEO
    # for chofer in lista_de_choferes:
    #     print("ID del chofer:")
    #     print(chofer.id_de_usuario_id)

    # Mensaje de debuggeo
    # print(user.id)

    # Aquí enviaré la lista de choferes, y cualquier otra ID qeu necesite
    return render(request, 'index.html', {
        "id_del_usuario_logueado": id_del_usuario_logueado,
        "lista_de_choferes": lista_de_choferes,
    })

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


""" Vista del Horario del Chofer Logueado.

SOLO LOS USUARIOS LOGUEADOS PUEDEN ENTRAR A ESTA PÁGINA.

Voy a ir imprimiendo el nombre del chofer en la página de horarios individuales. Prefiero agarrar el nombre de la tabla 
Chofer que de la Tabla Usuario.

Recuerda que no necesito la ID del a tabla Chofer, sino que necesito la ID DE USUARIO que está en la tabla Chofer
"""
@login_required
def horario_chofer_logueado(request):

    # Esto agarra los datos del chofer logueado
    chofer_logueado = Chofer.objects.get(id_de_usuario_id=request.user.id)

    # MENSAJE DE DEBUGGEO
    print("ID del chofer logueado")
    print(chofer_logueado)

    return render(request, 'horario_chofer_logueado.html', {
        "chofer_logueado": chofer_logueado,
    })

