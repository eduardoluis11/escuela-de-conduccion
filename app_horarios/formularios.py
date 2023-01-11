# Esto me deja usar los formularios de Django
from django import forms

# Esto me dejará agarrar fecha la fecha de hoy
from datetime import date

# Esto importará todos los modelos que he creado
from .models import User, Chofer, Secretario, Oficina, Asistencia, ReporteSemanal, Estudiante, HorariosLunes, \
    HorariosMartes, HorariosMiercoles, HorariosJueves, HorariosViernes, HorariosSabados, HorariosDomingos, \
    PeticionParaCambiarHorario, Semana, SemanaParaReportesSemanales

""" Formulario de Inicio de Sesión.

La contraseña tiene un widget que censurará la contraseña por motivos de seguridad.

Para evitar problemas con la base de datos, tengo que escribir "contrasena", no "contraseña".
"""
class FormularioInicioSesion(forms.Form):
    nombre_de_usuario = forms.CharField(max_length=100)
    contrasena = forms.CharField(max_length=2000, widget=forms.PasswordInput)   # Contraseña


""" Formulario para Agregar Horarios para ser usado por secretarios

Los campos que necesito son exactamente los mismos que los que aparecen en el modelo para agregar horarios. Claro, el 
timestamp se agregará solo y automáticamente.

Recuerda que hay horarios para cada día de la semana por separado.

No tengo que crear 7 paginas con 7 formularios para los horarios: creare menu select para escoger un dia de la semana 
(me sale lunes, martes... hasta domingo). Solo puedo escoger un dia. Si escojo lunes, todos esos datos del horario se 
meteran en la tabla HorariosLunes desde el view del formulario.  Si es martes, se meteran en la tabla del martes. Y 
asi sucesivamente.

Los campos que necesito son los siguientes:
•	Nombre del turno (ej: turno de jesus - 02 ene - 10 am a 12 pm ). X
•	ID del chofer (tomado como clave foranea). X
•	ID de la oficina (tomada como clave foranea). X 
•	ID del estudiante.  X
•	Día de la semana (Lunes, martes, etc) (saldrá de un menú)
•	Horario de inicio del turno. X
•	Horario de fin del turno. X
•	Semana del turno (tomado como clave foranea) X
•	Si se usará carro automático o sincrónico (saldrá de un menú) X

Usaré algo similar para agarrar los “Foreign keys”. Usaré “ModelChoiceField” para usar un Query Set y así agarrar los 
registros de las claves foráneas que necesito.
"""
class FormularioAgregarHorarios(forms.Form):

    # Lista de días de la semana de lunes a domingo
    OPCIONES_DIAS_DE_LA_SEMANA = (
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    )

    # Esta es la lista donde se almacena si el carro es automático o sincrónico
    OPCIONES_AUTOMATICO_O_SINCRONICO = (
        ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
        ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    )

    # Nombre del horario (ej: "Horario de Pedro Perez")
    nombre_del_horario = forms.CharField()

    # ID del chofer (tomado como clave foranea)
    chofer = forms.ModelChoiceField(queryset=Chofer.objects.all())

    # id_del_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_lunes",
    #                                   default=0)

    # Oficina a la que le pertenece este horario
    oficina = forms.ModelChoiceField(queryset=Oficina.objects.all())


    # id_de_oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
    #                                   related_name="oficina_a_la_que_le_pertenece_horario_lunes", default=0)

    # ID del estudiante
    estudiante = forms.ModelChoiceField(queryset=Estudiante.objects.all())

    # id_del_estudiante = models.ForeignKey("Estudiante", on_delete=models.CASCADE,
    #                                       related_name="id_de_estudiante_lunes",
    #                                       default=0)

    # Día de la semana
    dia_de_la_semana = forms.ChoiceField(choices=OPCIONES_DIAS_DE_LA_SEMANA)

    # Hora de entrada y salida del turno
    hora_de_inicio_del_turno = forms.TimeField()
    hora_de_fin_del_turno = forms.TimeField()

    # Semana del turno
    semana_del_turno = forms.ModelChoiceField(queryset=Semana.objects.all())

    # semana_del_turno = models.ForeignKey("Semana", on_delete=models.CASCADE,
    #                                      related_name="semana_del_turno_del_lunes",
    #                                      default=0)

    # Esto guarda si el estudiante usará un carro sincrónico o automático
    usara_carro_automatico_o_sincronico = forms.ChoiceField(choices=OPCIONES_AUTOMATICO_O_SINCRONICO)


