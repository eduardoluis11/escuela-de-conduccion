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
    HorariosMartes, HorariosMiercoles, HorariosJueves, HorariosViernes, HorariosSabados, HorariosDomingos, \
    PeticionParaCambiarHorario, Semana

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

Como la página de inicio es distinta para los choferes, el secretario, y si nadie se ha logueado, 
tengo que agarrar a todos los choferes, secretarios y al super usuario, y enviarlos por Jinja al index.html.

Para agarrar al super usuario (que necesito ver si el campo "isSuperUser = true"), voy a tener que agarrar una 
instancia del usuario logueado.
"""
def index(request):

    # Esto almacenará la ID del usuario si se loguea
    id_del_usuario_logueado = ''

    # Esto almacenará todos los datos del usuario si se loguea
    instancia_usuario_logueado = ''

    # Esto chequea si el usuario está logueado
    if request.user.is_authenticated:

        # Esto almacena la ID del usuario logueado como un integer
        id_del_usuario_logueado = int(request.user.id)

        # Esto agarra al usuario logueado
        instancia_usuario_logueado = User.objects.get(id=id_del_usuario_logueado)

        # MENSAJE DE DEBUGGEO
        # print("Esta es la ID del usuario logueado:")
        # print(id_del_usuario_logueado)


    # Esto agarra a todos los choferes
    lista_de_choferes = Chofer.objects.all()

    # Esto agarra todos los secretarios
    lista_de_secretarios = Secretario.objects.all()




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
        "lista_de_secretarios": lista_de_secretarios,
        "instancia_usuario_logueado": instancia_usuario_logueado,
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

Recuerda que no necesito la ID del a tabla Chofer, sino que necesito la ID DE USUARIO que está en la tabla Chofer.

Primero, debo hacer un bucle “for” para iterar todas las semanas de la tabla Semana.

Ahora, voy a imprimir todos los turnos en cada día. Voy a ordenarlos por hora de inicio (desde más temprano a más 
tarde). Pero antes, voy simplemente a imprimir los turnos. Para ello, agarraré todos los turnos de todas las tablas de 
todos los días, y los enviaré via Jinja.

Tengo que, al crear el query set que agarra todos los horarios, poner el filtro “order_by(campo_con_la_hora__hour')” al 
final del Query set para ordenar los horarios por orden de hora de inicio.

Los datos que necesito de otras tablas para imprimirlo en el horario son: los datos del Estudiante, y los datos de la 
Oficina. Entonces, con un Query Set, agarraré todos los datos de los modelos Estudiante y Oficina. Luego, compararé las 
IDs de los estudiantes y de las oficinas con las que están registradas en el turno. Si son las mismas, imprimiré esa 
oficina y ese estudiante.

Voy a ordenar las semanas por orden de fecha del lunes, en donde el lunes más reciente será la semana que aparezca de 
primero. Para arreglar algo por orden descendiente, debo usar ‘order_by’ y ‘-nombre_del_campo’.
"""
@login_required
def horario_chofer_logueado(request):

    # Esto agarra los datos del chofer logueado
    chofer_logueado = Chofer.objects.get(id_de_usuario_id=request.user.id)

    # MENSAJE DE DEBUGGEO
    # print("ID del chofer logueado")
    # print(chofer_logueado)

    # Esto almacenará la ID del usuario si se loguea
    id_del_usuario_logueado = ''

    # Esto almacena la ID del usuario logueado
    id_del_usuario_logueado = int(request.user.id)

    # Esto agarra las IDs de todos los choferes
    lista_de_choferes = Chofer.objects.all()

    # Esto agarra todas las semanas en la tabla Semana
    lista_de_semanas = Semana.objects.all().order_by('-fecha_del_lunes')

    # Esto agarrará todos los turnos del lunes
    turnos_lunes = HorariosLunes.objects.all().order_by('hora_de_inicio_del_turno__hour')

    # Turnos del martes
    turnos_martes = HorariosMartes.objects.all().order_by('hora_de_inicio_del_turno__hour')

    # Esto agarrará todos los turnos del resto de los días
    turnos_miercoles = HorariosMiercoles.objects.all().order_by('hora_de_inicio_del_turno__hour')
    turnos_jueves = HorariosJueves.objects.all().order_by('hora_de_inicio_del_turno__hour')
    turnos_viernes = HorariosViernes.objects.all().order_by('hora_de_inicio_del_turno__hour')
    turnos_sabado = HorariosSabados.objects.all().order_by('hora_de_inicio_del_turno__hour')
    turnos_domingo = HorariosDomingos.objects.all().order_by('hora_de_inicio_del_turno__hour')

    # Esto agarra todos los estudiantes
    estudiantes = Estudiante.objects.all()

    # Esto agarra todas las oficinas
    oficinas = Oficina.objects.all()

    # # MENSAJE DE DEBUGGEO:
    # print("Estudiantes relacionados al turno del lunes:")
    #
    # # Esto agarrará un estudiante de ejemplo
    # estudiante_de_ejemplo = Estudiante.objects.get(id=1)
    #
    # # MENSAJE DE DEBUGGEO
    # print(turno_lunes_de_ejemplo_chofer_logueado.id_de_estudiante_lunes.all())


    # print(turnos_lunes.id_de_estudiante_lunes.all())

    return render(request, 'horario_chofer_logueado.html', {
        "chofer_logueado": chofer_logueado,
        "id_del_usuario_logueado": id_del_usuario_logueado,
        "lista_de_choferes": lista_de_choferes,
        "lista_de_semanas": lista_de_semanas,
        "turnos_lunes": turnos_lunes,
        "turnos_martes": turnos_martes,
        "turnos_miercoles": turnos_miercoles,
        "turnos_jueves": turnos_jueves,
        "turnos_viernes": turnos_viernes,
        "turnos_sabado": turnos_sabado,
        "turnos_domingo": turnos_domingo,
        "estudiantes": estudiantes,
        "oficinas": oficinas,

    })

""" Vista con la Lista de Fechas en las que hay Reportes Semanales Registrados.

Hay que estar logueado para poder entrar a esta página.

Todos los secretarios deben poder ver todos los reportes. Por lo tanto, no tengo que poner ninguna restricción aquí. 
Solo debo poner las fechas de los reportes en orden descendiente (del mas nuevo al mas viejo).
"""
@login_required
def lista_fechas_reportes_semanales(request):

    # Esto almacena la ID del usuario logueado
    id_del_usuario_logueado = int(request.user.id)

    # Esto agarra todos los secretarios
    lista_de_secretarios = Secretario.objects.all()

    # Esto agarra al usuario logueado
    instancia_usuario_logueado = User.objects.get(id=request.user.id)

    # Esto agarra todos los reportes semanales

    return render(request, './reportes_semanales/lista_fechas_reportes_semanales.html', {
        "lista_de_secretarios": lista_de_secretarios,
        "instancia_usuario_logueado": instancia_usuario_logueado,
        "id_del_usuario_logueado": id_del_usuario_logueado,
    })
