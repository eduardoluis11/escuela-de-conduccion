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

# Esto me dejará agarrar la fecha y la hora actual
import datetime

# Esto importará todos los modelos que he creado
from .models import User, Chofer, Secretario, Oficina, Asistencia, ReporteSemanal, Estudiante, HorariosLunes, \
    HorariosMartes, HorariosMiercoles, HorariosJueves, HorariosViernes, HorariosSabados, HorariosDomingos, \
    PeticionParaCambiarHorario, Semana, SemanaParaReportesSemanales

# Esto me dejará usar los formularios de Django de formularios.py
from .formularios import FormularioInicioSesion, FormularioAgregarHorarios


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

En el index hay que hacer varias cosas para agregarle ciberseguridad, ya que hay 3 páginas posibles: si el usuario no 
esta logueado, si se mete un secretario o un administrador, o si se mete un chofer. Mira el “return render()”, ya que 
me debe renderizar algo, este o no esté logueado el usuario. Si el usuario no está logueado, siempre se debe 
renderizar la página.
"""
def index(request):

    # Esto almacenará la ID del usuario si se loguea
    id_del_usuario_logueado = ''

    # Esto almacenará todos los datos del usuario si se loguea
    instancia_usuario_logueado = ''

    # Esto agarra a todos los choferes
    lista_de_choferes = Chofer.objects.all()

    # Esto agarra todos los secretarios
    lista_de_secretarios = Secretario.objects.all()


    # Esto chequea si el usuario está logueado
    if request.user.is_authenticated:

        # Esto almacena la ID del usuario logueado como un integer
        id_del_usuario_logueado = int(request.user.id)

        # Esto agarra al usuario logueado
        instancia_usuario_logueado = User.objects.get(id=id_del_usuario_logueado)

        # MENSAJE DE DEBUGGEO
        # print("Esta es la ID del usuario logueado:")
        # print(id_del_usuario_logueado)

        # Esto me va a renderizar la página para los choferes
        for chofer in lista_de_choferes:
            if id_del_usuario_logueado == chofer.id_de_usuario_id:

                # Aquí enviaré la lista de choferes, y cualquier otra ID que necesite
                return render(request, 'index.html', {
                    "id_del_usuario_logueado": id_del_usuario_logueado,
                    "lista_de_choferes": lista_de_choferes,

                    "instancia_usuario_logueado": instancia_usuario_logueado,
                })

        # Esto me va a renderizar la página para el administrador y el secretario en horario de trabajo
        for secretario in lista_de_secretarios:
            if id_del_usuario_logueado == secretario.id_de_usuario_id and secretario.esta_dentro_del_horario_de_trabajo is True or instancia_usuario_logueado.is_superuser == 1:

                # Aquí enviaré la lista de choferes, y cualquier otra ID que necesite
                return render(request, 'index.html', {
                    "id_del_usuario_logueado": id_del_usuario_logueado,

                    "lista_de_secretarios": lista_de_secretarios,
                    "instancia_usuario_logueado": instancia_usuario_logueado,
                })

        # Si el usuario no es ni chofer, ni administrador, ni secretario en horario de trabajo, le mostraré un error
        return render(request, 'error.html')

    # Si el usuario no está logueado, igual renderizaré la página de inicio
    else:

        # Bucle de DEBUGGEO
        # for chofer in lista_de_choferes:
        #     print("ID del chofer:")
        #     print(chofer.id_de_usuario_id)

        # Mensaje de debuggeo
        # print(user.id)

        # Esto renderiza la pág de inicio si el usuario no se ha logueado
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

Ahora, solo me falta agregarle ciberseguridad a la página de horarios individuales de los choferes, para que ni el 
administrador ni los secretarios (dentro o fuera de horario) no puedan entrar a los horarios individuales. Solo los 
choferes podrán entrar a la página de sus horarios.

Con tan solo poner un “if usuario es chofer, renderiza la página. Else, renderiza la página con el mensaje de error” 
debería ser suficiente para agregar ciberseguridad.
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

    # Esto chequea si el usuario que se logueó es un chofer
    for chofer in lista_de_choferes:
        if id_del_usuario_logueado == chofer.id_de_usuario_id:

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

        # Si el usuario no es un chofer, le mostraré un mensaje de error
        else:
            return render(request, 'error.html')

""" Vista con la Lista de Fechas en las que hay Reportes Semanales Registrados.

Hay que estar logueado para poder entrar a esta página.

Todos los secretarios deben poder ver todos los reportes. Por lo tanto, no tengo que poner ninguna restricción aquí. 
Solo debo poner las fechas de los reportes en orden descendiente (del mas nuevo al mas viejo).

Entonces, pondré 3 restricciones para ver los reportes semanales: que el usuario sea secretario Y que esté dentro del 
horario de trabajo, o que el usuario sea el administrador. Para que el usuario esté dentro de la hora de trabajo, solo 
debo asegurarme de que el campo "esta dentro del horario" sea “true”.
"""
@login_required
def lista_fechas_reportes_semanales(request):

    # Esto almacena la ID del usuario logueado
    id_del_usuario_logueado = int(request.user.id)

    # Esto agarra todos los secretarios
    lista_de_secretarios = Secretario.objects.all()

    # Esto agarra al usuario logueado
    instancia_usuario_logueado = User.objects.get(id=request.user.id)

    # Esto chequea si el usuario es un secretario en horario de trabajo, o un administrador
    for secretario in lista_de_secretarios:
        if id_del_usuario_logueado == secretario.id_de_usuario_id and secretario.esta_dentro_del_horario_de_trabajo is True or instancia_usuario_logueado.is_superuser == 1:

            # La página funcionará como debe si un secretario se loguea

            # Esto agarra todas las fechas para los reportes semanales
            lista_de_fechas_reportes_semanales = SemanaParaReportesSemanales.objects.all()

            return render(request, './reportes_semanales/lista_fechas_reportes_semanales.html', {
                "lista_de_secretarios": lista_de_secretarios,
                "instancia_usuario_logueado": instancia_usuario_logueado,
                "id_del_usuario_logueado": id_del_usuario_logueado,
                "lista_de_fechas_reportes_semanales": lista_de_fechas_reportes_semanales,
            })

        # Si se loguea un chofer o un secretario despues de las 7 pm, saldrá un mensaje de error
        else:
            return render(request, 'error.html')



""" Vista de Lista de Reportes Semanales de la Semana Seleccionada.

Debes estar logueado para ver esta página.

Aquí saldrán los reportes semanales de todos los choferes para la semana seleccionada.

Dado a que cada semana tiene una lista de reportes distinta, es decir, que voy a tener que generar un monton de páginas
de manera dinámica, tendré que agregar la ID de la semana seleccionada a la URL de la página con la lista de reportes
semanales.

Voy a renderizar la página SOLO cuando una ID de una semana existente haya sido seleccionada. De lo contrario, me debe 
salir un mensaje de error. 

Tengo que primero agarrar todas las semanas de la tabla de Semanas para Reportes Semanales.

Ahora, necesito agarrar todos los reportes de que pertenezcan a una semana en específico, y debo mostrarlo en la página 
de Lista de Reportes de esa fecha. Primero, necesito imprimir la fecha del lunes y la fecha del domingo de esa semana 
en el título <h1> de la página.

“id_de_semana_id” es la ID de la semana a la que pertenecen varios reportes.

Prefiero usar "semana_seleccionada.id" que "semana_id" en la lista de reportes semanales por motivos de seguridad.
Así, debería salir un error si el usuario escribe una ID de una semana que no exista en la base de datos.
"""
@login_required
def lista_reportes_semanales_semana_seleccionada(request, semana_id):

    # Esto almacena la ID del usuario logueado
    id_del_usuario_logueado = int(request.user.id)

    # Esto agarra todos los secretarios
    lista_de_secretarios = Secretario.objects.all()

    # Esto agarra al usuario logueado
    instancia_usuario_logueado = User.objects.get(id=request.user.id)

    # Esto chequea si el usuario es un secretario en horario de trabajo, o un administrador
    for secretario in lista_de_secretarios:
        if id_del_usuario_logueado == secretario.id_de_usuario_id and secretario.esta_dentro_del_horario_de_trabajo is True or instancia_usuario_logueado.is_superuser == 1:


            # Esto agarra la semana seleccionada
            semana_seleccionada = SemanaParaReportesSemanales.objects.get(id=semana_id)

            # Esto agarra TODOS los reportes semanales de la semana seleccionada
            lista_reportes_semanales = ReporteSemanal.objects.filter(id_de_semana_id=semana_seleccionada.id)

            # Esto agarra todos los choferes
            lista_de_choferes = Chofer.objects.all()

            # print("Esta es la ID de la semana seleccionada:")
            # print(lista_reportes_semanales)

            # # MENSAJE DE DEBUGGEO
            # print("Lista de reportes de la semana seleccionada:")
            # print(lista_reportes_semanales)

            return render(request, './reportes_semanales/reportes_semanales_semana_seleccionada.html', {
                "lista_reportes_semanales": lista_reportes_semanales,
                "semana_seleccionada": semana_seleccionada,
                "lista_de_choferes": lista_de_choferes,
                "id_del_usuario_logueado": id_del_usuario_logueado,
                "lista_de_secretarios": lista_de_secretarios,

            })

        # Si el usuario no es administrador ni un secretario en horario de trabajo, mostrarles un error
        else:
            return render(request, 'error.html')


""" Vista Detallada de un Reporte Semanal. 

Necesito el ID del reporte a ver de forma detallada, ya que el secretario puede ver un montón de reportes.

Luego veré si agrego un botón para mostrar una página con un formulario para que los secretarios agreguen nuevos
reportes semanales.
"""
@login_required
def reporte_semanal(request, reporte_id):

    # Esto almacena la ID del usuario logueado
    id_del_usuario_logueado = int(request.user.id)

    # Esto agarra todos los secretarios para revisar si esta logueado
    lista_de_secretarios = Secretario.objects.all()

    # Esto agarra al usuario logueado
    instancia_usuario_logueado = User.objects.get(id=request.user.id)

    # Esto chequea si el usuario es un secretario en horario de trabajo, o un administrador
    for secretario in lista_de_secretarios:
        if id_del_usuario_logueado == secretario.id_de_usuario_id and secretario.esta_dentro_del_horario_de_trabajo is True or instancia_usuario_logueado.is_superuser == 1:

            # Esto agarra todos los choferes
            lista_de_choferes = Chofer.objects.all()

            # Reporte semanal que quiero mostrar
            reporte_semanal_seleccionado = ReporteSemanal.objects.get(id=reporte_id)

            return render(request, './reportes_semanales/reporte_semanal_detallado.html', {
                "lista_de_choferes": lista_de_choferes,
                "reporte_semanal_seleccionado": reporte_semanal_seleccionado,

                # Estas 2 lineas las necesito para renderizar enlaces en navbar y footer
                "id_del_usuario_logueado": id_del_usuario_logueado,
                "lista_de_secretarios": lista_de_secretarios,

            })

        # Si el usuario no es administrador ni un secretario en horario de trabajo, mostrarles un error
        else:
            return render(request, 'error.html')


""" Vista de Formulario para que lso secretarios puedan Agregar Horarios.

Debo detectar un Post request. Si detecta el Post request, meteré los datos de los campos en una de las 7 tablas de los 
horarios con el nuevo turno.

Y, por razones de seguridad, solo detectaré el POST request si el usuario logueado es un secretario.

Si no se detecta un POST request, renderizaré como si nada la página con el formulario.

Puedo redirigir al usuario al home page después de agregar un horario, y le mostraré un mensaje flash de confirmación, 
para así mostrarle que se agregó un horario.

Voy a meter los datos en la base de datos para agregar un horario. Recuerda que, dependiendo del día escogido (lunes, 
martes, etc), lo meteré en la tabla correspondiente (HorariosLunes, HorariosMartes, etc).

Dado a que usaré 7 casos (uno por cada día de la semana), prefiero usar un match/case, para que así sea más fácil.
de leer. Dentro del “match” pondré la variable que quiero comparar, mientras que en “case” pondré si es lunes, o 
martes, etc.

Los campos del formulario de agregar horarios que están agarrando con un Query Set los distintos choferes, oficinas, 
etc, están agarrando la ID de ese chofer u oficina seleccionados. Y la cosa es que los están agarrando como un string. 
Entonces, lo bueno es que están agarrando la ID. Lo malo es que stán como un string. Entonces, para los campos que me 
están agarrando los registros de tablas (como choferes u oficinas), primero voy a convertir esas variables a Integer. 
LUEGO, las meteré en la base de datos.

Ya vi como agregar los mensajes de confirmación usando “messages”. Primero, debo importar la biblioteca “messages” en 
views.py. Luego, debo crear el mensaje flash de confirmación usando “messages”. Después, en el archivo HTML, uso un 
bucle “for” para agarrar cada mensaje en “messages” (que es un tipo de array), e imprimo el mensaje de confirmación.
"""
@login_required
def agregar_horarios(request):

    # Esto importa el formulario de Django de agregar horarios
    formulario = FormularioAgregarHorarios()

    # Esto almacena la ID del usuario logueado
    id_del_usuario_logueado = int(request.user.id)

    # Esto agarra todos los secretarios para revisar si esta logueado
    lista_de_secretarios = Secretario.objects.all()

    # Esto agarra al usuario logueado
    instancia_usuario_logueado = User.objects.get(id=request.user.id)

    # Esto chequea si el usuario es un secretario en horario de trabajo, o un administrador
    for secretario in lista_de_secretarios:
        if id_del_usuario_logueado == secretario.id_de_usuario_id and secretario.esta_dentro_del_horario_de_trabajo is True or instancia_usuario_logueado.is_superuser == 1:

            # Esto detecta si el usuario ha entregado el formulario, es decir, si hizo un POST request
            if request.method == "POST":

                # Voy primero a agarrar los datos de cada casilla del formulario
                nombre_del_horario = request.POST["nombre_del_horario"]
                chofer = int(request.POST["chofer"])
                oficina = int(request.POST["oficina"])
                estudiante = int(request.POST["estudiante"])
                dia_de_la_semana = request.POST["dia_de_la_semana"]
                hora_de_inicio_del_turno = request.POST["hora_de_inicio_del_turno"]
                hora_de_fin_del_turno = request.POST["hora_de_fin_del_turno"]
                semana_del_turno = int(request.POST["semana_del_turno"])
                usara_carro_automatico_o_sincronico = request.POST["usara_carro_automatico_o_sincronico"]

                # Esto agarra la fecha y hora actual
                fecha_y_hora_en_la_que_se_registro_turno = datetime.datetime.now()

                # # DEBUGGEO: Quiero ver que se está metiendo en los campos con los registros (choferes, oficinas, etc)
                # print("Esto es lo que contiene el campo 'chofer': ")
                # print(chofer)

                # Dependiendo del día de la semana escogido, voy a meter los datos en una tabla u otra. ...
                match dia_de_la_semana:

                    # Si el día es lunes, lo meteré en los Horarios del Lunes
                    case "Lunes":

                        # Esto prepara los datos antes de meterlos a la base de datos
                        nuevo_turno = HorariosLunes(nombre_del_horario=nombre_del_horario,
                                                    hora_de_inicio_del_turno=hora_de_inicio_del_turno,
                                                    hora_de_fin_del_turno=hora_de_fin_del_turno,
                                                    fecha_y_hora_en_la_que_se_registro_turno=fecha_y_hora_en_la_que_se_registro_turno,
                                                    usara_carro_automatico_o_sincronico=usara_carro_automatico_o_sincronico,
                                                    id_del_chofer_id=chofer, id_de_oficina_id=oficina,
                                                    id_del_estudiante_id=estudiante,
                                                    semana_del_turno_id=semana_del_turno)

                        # Esto termina de meter los datos en la base de datos
                        nuevo_turno.save()

                    # Martes
                    case "Martes":

                        # Esto prepara los datos antes de meterlos a la base de datos
                        nuevo_turno = HorariosMartes(nombre_del_horario=nombre_del_horario,
                                                    hora_de_inicio_del_turno=hora_de_inicio_del_turno,
                                                    hora_de_fin_del_turno=hora_de_fin_del_turno,
                                                    fecha_y_hora_en_la_que_se_registro_turno=fecha_y_hora_en_la_que_se_registro_turno,
                                                    usara_carro_automatico_o_sincronico=usara_carro_automatico_o_sincronico,
                                                    id_del_chofer_id=chofer, id_de_oficina_id=oficina,
                                                    id_del_estudiante_id=estudiante,
                                                    semana_del_turno_id=semana_del_turno)

                        # Esto termina de meter los datos en la base de datos
                        nuevo_turno.save()

                    # Miércoles
                    case "Miércoles":

                        # Esto prepara los datos antes de meterlos a la base de datos
                        nuevo_turno = HorariosMiercoles(nombre_del_horario=nombre_del_horario,
                                                    hora_de_inicio_del_turno=hora_de_inicio_del_turno,
                                                    hora_de_fin_del_turno=hora_de_fin_del_turno,
                                                    fecha_y_hora_en_la_que_se_registro_turno=fecha_y_hora_en_la_que_se_registro_turno,
                                                    usara_carro_automatico_o_sincronico=usara_carro_automatico_o_sincronico,
                                                    id_del_chofer_id=chofer, id_de_oficina_id=oficina,
                                                    id_del_estudiante_id=estudiante,
                                                    semana_del_turno_id=semana_del_turno)

                        # Esto termina de meter los datos en la base de datos
                        nuevo_turno.save()

                    # Jueves
                    case "Jueves":

                        # Esto prepara los datos antes de meterlos a la base de datos
                        nuevo_turno = HorariosJueves(nombre_del_horario=nombre_del_horario,
                                                    hora_de_inicio_del_turno=hora_de_inicio_del_turno,
                                                    hora_de_fin_del_turno=hora_de_fin_del_turno,
                                                    fecha_y_hora_en_la_que_se_registro_turno=fecha_y_hora_en_la_que_se_registro_turno,
                                                    usara_carro_automatico_o_sincronico=usara_carro_automatico_o_sincronico,
                                                    id_del_chofer_id=chofer, id_de_oficina_id=oficina,
                                                    id_del_estudiante_id=estudiante,
                                                    semana_del_turno_id=semana_del_turno)

                        # Esto termina de meter los datos en la base de datos
                        nuevo_turno.save()

                    # Viernes
                    case "Viernes":

                        # Esto prepara los datos antes de meterlos a la base de datos
                        nuevo_turno = HorariosViernes(nombre_del_horario=nombre_del_horario,
                                                    hora_de_inicio_del_turno=hora_de_inicio_del_turno,
                                                    hora_de_fin_del_turno=hora_de_fin_del_turno,
                                                    fecha_y_hora_en_la_que_se_registro_turno=fecha_y_hora_en_la_que_se_registro_turno,
                                                    usara_carro_automatico_o_sincronico=usara_carro_automatico_o_sincronico,
                                                    id_del_chofer_id=chofer, id_de_oficina_id=oficina,
                                                    id_del_estudiante_id=estudiante,
                                                    semana_del_turno_id=semana_del_turno)

                        # Esto termina de meter los datos en la base de datos
                        nuevo_turno.save()

                    # Sábado
                    case "Sábado":

                        # Esto prepara los datos antes de meterlos a la base de datos
                        nuevo_turno = HorariosSabados(nombre_del_horario=nombre_del_horario,
                                                    hora_de_inicio_del_turno=hora_de_inicio_del_turno,
                                                    hora_de_fin_del_turno=hora_de_fin_del_turno,
                                                    fecha_y_hora_en_la_que_se_registro_turno=fecha_y_hora_en_la_que_se_registro_turno,
                                                    usara_carro_automatico_o_sincronico=usara_carro_automatico_o_sincronico,
                                                    id_del_chofer_id=chofer, id_de_oficina_id=oficina,
                                                    id_del_estudiante_id=estudiante,
                                                    semana_del_turno_id=semana_del_turno)

                        # Esto termina de meter los datos en la base de datos
                        nuevo_turno.save()

                    # Domingo
                    case "Domingo":

                        # Esto prepara los datos antes de meterlos a la base de datos
                        nuevo_turno = HorariosDomingos(nombre_del_horario=nombre_del_horario,
                                                    hora_de_inicio_del_turno=hora_de_inicio_del_turno,
                                                    hora_de_fin_del_turno=hora_de_fin_del_turno,
                                                    fecha_y_hora_en_la_que_se_registro_turno=fecha_y_hora_en_la_que_se_registro_turno,
                                                    usara_carro_automatico_o_sincronico=usara_carro_automatico_o_sincronico,
                                                    id_del_chofer_id=chofer, id_de_oficina_id=oficina,
                                                    id_del_estudiante_id=estudiante,
                                                    semana_del_turno_id=semana_del_turno)

                        # Esto termina de meter los datos en la base de datos
                        nuevo_turno.save()


                # Mensaje flash de confirmación
                messages.success(request, "Se ha agregado correctamente un nuevo turno para un horario.")

                # Esto va a redirigir al usuario al home page
                return HttpResponseRedirect(reverse("index"))

            # Esto renderiza la página si el usuario no ha entregado el formulario con un POST
            else:
                return render(request, './horarios_secretarios/formulario_agregar_horarios.html', {
                    "formulario": formulario,
                    # Estas 2 lineas las necesito para renderizar enlaces en navbar y footer
                    "id_del_usuario_logueado": id_del_usuario_logueado,
                    "lista_de_secretarios": lista_de_secretarios,
                })

        # Si el usuario no es administrador ni un secretario en horario de trabajo, mostrarles un error
        else:
            return render(request, 'error.html')

""" Vista de Mensaje de Error.

Esto saldrá si el usuario entra a una página que no debería (por ejemplo, si el chofer intenta entrar a páginas
que son solo para secretarios).

El usuario debe pdoer ver esto, esté logueado o no.
"""
def mensaje_de_error(request):
    return render(request, 'error.html')
