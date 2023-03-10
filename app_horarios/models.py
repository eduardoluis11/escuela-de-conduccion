from django.db import models

# Esto es para agregar la fecha actual
from datetime import date

""" Para registrar usuarios y dejarles que inicien sesión, voy a usar la biblioteca "Abstract User", ya que me deja 
hacer esto muy rápidamente (fuente: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/).

ESTO ME ARREGLO UN BUG QUE NO ME DEJABA CREAR LA BBDD PORQUE NO DETECTABA EL MODELO "User".
"""
from django.contrib.auth.models import AbstractUser

# Inserta aquí tus modelos

""" Modelo para almacenar usuarios (fuente: https://docs.djangoproject.com/en/4.1/topics/auth/customizing/).

Esto me dejará tanto registrar usuarios, como dejarles iniciar sesión.
"""


class User(AbstractUser):
    pass


""" Modelo de los Choferes

Los datos serán:
•	Nombre
•	Apellidos
•	Email
•	Documento nacional de identidad (DNI).
•	Teléfono
•	Dirección
•	Codigo ID del usuario (clave foránea del usuario).

Idealmente debería almacenar el DNI de los choferes. Voy a poner el DNI como opcional, tanto para los choferes como 
para los estudiantes, en caso de que la compañía no quiera almacenar esos datos tan delicados.

Para arreglar el nombre en plural de las tablas en el panel del admin, usaré "Meta" y "verbose name plural". Ahi, 
pondré manualmente escribiré como quiero que se vea el nombre en plural.
"""


class Chofer(models.Model):
    # ID del chofer (tomado como clave foranea)
    id_de_usuario = models.ForeignKey("User", on_delete=models.CASCADE, related_name="id_de_usuario_de_chofer")

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True, max_length=20)
    email = models.EmailField(blank=True, null=True, max_length=254)

    # Esto le cambiara el titulo a cada registro de la tabla
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    # Nombre en plural arreglado en el panel del administrador
    class Meta:
        verbose_name_plural = "Choferes"


""" Modelo de Secretarios/as 	

Lo que voy a hacer es una tabla llamada “secretarios”, en los cuales meteré a algunos usuarios y les daré el status de 
“secretario” con un booleano. Si son secretarios, podrán ver las páginas con los datos de los choferes y los reportes, 
A PESAR DE que no puedan entrar en el panel del admin. 

En el modelo de “Secretario”, pondré que usuario que no sea super usuario pueda ver los reportes semanales y otros 
datos. Pondré la ID del usuario a través de una clave foránea, su nombre de usuario (clave foránea del usuario), y si 
el usuario es secretario o no (mediante un booleano).

Si el usuario es secretario (el booleano es “True”), ellos, junto con los súper usuarios, podrán ver los reportes 
semanales y otros datos privados de la web app.

Los datos que necesito para la tabla “Secretario” son:
•	ID del usuario (tomada como clave foránea de User)
•	Si el usuario es secretario o no (booleano)

Si el usuario ha sido agregado a esta tabla, entonces siempre será un secretario. Entonces, en el campo que pregunta
si es secretario o no SIEMPRE se debe dejar en "True".

Como le puse “True” como valor por defecto, el administrador no tendrá que tocar nada cuando seleccione al usuario para 
convertirlo en secretario. Solo tendrá que escoger la ID del usuario al que quiere convertir en secretario.

Sí, si se puede usar un menú de selección para un modelo. Simplemente tengo que crear una lista de Python, usar 
model.CharField, y meter el atributo “choices” dentro de ese CharField.

Voy a agregar un campo que dice si está dentro del horario de trabajo (por ejemplo, que si el secretario está conectado
antes de las 7 pm). Ese campo es para que el secretario no pueda hacer nada después de las 7 pm. Ese campo será un
booleano (true o false). No le veo la necesidad de convertirlo en un "sí o no", ya que nadie va a tocar esto. El único
que debería tocar esto es un script que crearé que, junto con un cron, van a cambiar ese booleano a "false" cuando
sean las 7 pm, para que así el secretario no pueda hacer nada.
"""


class Secretario(models.Model):
    OPCIONES_SI_O_NO = (
        ('Sí', 'Sí'),
        ('No', 'No'),
    )

    # ID del chofer (tomado como clave foranea)
    id_de_usuario = models.ForeignKey("User", on_delete=models.CASCADE, related_name="id_de_usuario_de_secretario")

    # Si el usuario es secretario (SIEMPRE DEJARLO EN "True")
    # el_usuario_es_secretario = models.BooleanField(default=True)

    # Si el usuario es secretario (SIEMPRE DEJARLO EN "Sí")
    el_usuario_es_secretario = models.CharField(max_length=2, choices=OPCIONES_SI_O_NO)

    # Esto es una restricción que usaré después para que el secretario no pueda hacer nada después de las 7 pm
    esta_dentro_del_horario_de_trabajo = models.BooleanField(default=True)

    # Esto le cambiara el titulo a cada registro de la tabla
    def __str__(self):
        return f"{self.id_de_usuario}"


""" Modelo de los Estudiantes

Los datos que necesito para el modelo de Estudiantes son:
•	DNI. X
•	Nombre. X
•	Apellidos. X
•	Número de teléfono (OPCIONAL). X
•	Email (opcional). X
•	Direccion (opcional). X
•	Si tiene carro automático o sincrónico (solo 2 opciones). X

Lo del email es para poder contactar el estudiante si no tiene teléfono. 

La dirección es para tener más o menos una idea de que tan cerca vive de cada oficina. Pero será opcional.

Despues de pensarlo mejor, que si el estudiante usará un carro sincrónico o automático va mejor ponerlo en los horarios
que en la tabla de Estudiantes.
"""


class Estudiante(models.Model):
    # # Esta es la lista donde se almacena si el carro es automático o sincrónico
    # OPCIONES_AUTOMATICO_O_SINCRONICO = (
    #     ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
    #     ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    # )

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True, max_length=20)
    email = models.EmailField(blank=True, null=True, max_length=254)

    # # Esto guarda si el estudiante usará un carro sincrónico o automático
    # usara_carro_automatico_o_sincronico = models.CharField(max_length=20, choices=OPCIONES_AUTOMATICO_O_SINCRONICO)

    # Esto mostrara el nombre del estudiante como el titulo de cada registro de la tabla
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


""" Modelo de Oficinas.

Los datos que necesito para el modelo de Oficinas son:
•	Nombre de la oficina.
•	Dirección de la oficina.
•	Los choferes que trabajan ahí.


Creo que tendré que crear una tabla extra para poner los choferes que trabajan en esa oficina y los horarios de los 
choferes en esa oficina. Eso se debe  a que quiero hacer que un chofer pueda trabajar en varias oficinas, y obviamente 
en una oficina pueden trabajar muchos choferes por lo que hay una relación de muchos a muchos entre choferes y 
oficinas. Entonces, tendré que usar un many-to-many relationship al crear el modelo. 

"""


class Oficina(models.Model):
    nombre_de_oficina = models.CharField(max_length=255)
    direccion = models.TextField()

    # Choferes que trabajan en esta oficina
    chofer = models.ManyToManyField(Chofer, blank=True, related_name="choferes_que_trabajan_en_oficina", default=[0])

    # Esto le cambiara el titulo a cada registro de la tabla
    def __str__(self):
        return f"{self.nombre_de_oficina}"

    # # Horarios de los choferes de la oficina
    # horario = models.ForeignKey("Horario", on_delete=models.CASCADE, related_name="id_de_chofer")


""" Modelo de Asistencias.

Solo me interesan las asistencias de los choferes, NO de los secretarios ni de los administradores (por los momentos).

El problema de crear una tabla por separado para las Fechas de Asistencias es que el administrador tendrá que 
primeramente agregar la fecha en la tabla “Fecha de Asistencia”, que es contra-intuitivo, y muy propenso a errores. 
Entonces, para que sea más fácil e intuitivo de usar, NO haré un modelo por separado para las fechas.  En su lugar, 
haré únicamente la tabla de Asistencia.

Para las Asistencias de cada día (el modelo), los datos que usaré son los siguientes:
•	ID del chofer.
•	Fecha en la que se está tomando la asistencia.
•	Si el chofer vino a trabajar (“sí” o “no”).
•	Horas trabajadas por el chofer (en números).
•	Fecha y hora en la que se registró esta asistencia (esto es automático) (Timestamp).

"""


class Asistencia(models.Model):
    # Esto lo usaré para decir si el chofer vino a trabajar o no
    OPCIONES_SI_O_NO = (
        ('Sí', 'Sí'),
        ('No', 'No'),
    )

    # se le asigna un nombre al reporte para encontrar facilmente el reporte de la asistencia
    nombre_de_reporte_de_asistencia = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_de_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_para_asistencia",
                                     default=0)

    # Fecha en la que se está tomando la asistencia
    fecha = models.DateField(default=date.today)

    # Si el chofer fue a trabajar o no
    vino_a_trabajar = models.CharField(max_length=2, choices=OPCIONES_SI_O_NO, default='Sí')

    # Horas trabajadas por el chofer
    horas_trabajadas = models.IntegerField(default=0)

    # Fecha y hora en la que se registró esta asistencia (Timestamp)
    fecha_y_hora_en_la_que_se_registro_asistencia = models.DateTimeField(auto_now_add=True)

    # fecha_y_hora_en_la_que_se_registro_asistencia = models.DateTimeField(default=date.today)

    # Esto le cambiara el titulo a cada registro de la tabla

    def __str__(self):
        return f"{self.nombre_de_reporte_de_asistencia}"


""" Modelo de los Reportes Semanales.

El modelo de Reporte Semanal tendrá los siguientes datos:
•	ID del chofer (tomada como clave foránea). X
•	Nombre del reporte semanal (ej: reporte del 1/1/23 de Pedro Perez). X
•	Fecha de inicio de la semana. X
•	Fecha de fin de la semana a evaluar. X
•	Horas de clases dadas durante la semana (ESTO NO SE PUEDE EDITAR. ESTO SE CALCULA AUTOMÁTICAMENTE). X
•	Número de clases canceladas durante la semana (ESTO NO SE PUEDE EDITAR. ESTO SE CALCULA AUTOMÁTICAMENTE).   X
•	Clases cambiadas a otro horario (OPCIONAL, y usare un <textarea> para esto). X
•	Motivos de las inasistencias (si las tiene) (OPCIONAL y con <textarea>).    X
•	Marca de tiempo para saber fecha y hora de cuando se creó este registro (Timestamp). X

Agarraré el cálculo de las horas trabajadas y las clases canceladas por ese chofer durante esa semana usando un Query 
Set, y lo meteré en una variable. Luego, meteré esa variable dentro del atributo “default” de tanto las horas 
trabajadas como de las clases canceladas.

Crearé el campo como clave foránea de la semana a seleccionar para la tabla “Reportes Semanales”. La clave foránea se 
tomará de la tabla “Semanas para Reportes Semanales”.
"""
class ReporteSemanal(models.Model):
    # # Variable de prueba para DEBUGGEO
    # numero_aleatorio = 40

    # # Mensaje de DEBUGGEO
    # print("Hola mundo")

    # Se le asigna un nombre al reporte para encontrar facilmente el reporte de la asistencia
    nombre_de_reporte_semanal = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_de_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_chofer_para_reporte_semanal",
                                     default=0)

    # ID de la semana a evaluar
    id_de_semana = models.ForeignKey("SemanaParaReportesSemanales", on_delete=models.CASCADE,
                                     related_name="id_semana_para_reporte_semanal",
                                     default=0)

    # # Query Set que agarrará todos los días en el que el chofer no haya venido a trabajar
    # Asistencia.objects.filter(user_id=id_de_chofer)

    # Fecha de inicio de la semana a evaluar
    fecha_de_inicio_de_semana_a_evaluar = models.DateField(default=date.today)

    # Fecha del final de la semana a evaluar
    fecha_final_de_semana_a_evaluar = models.DateField(default=date.today)

    # Clases cambiadas a otro horario
    clases_cambiadas_a_otro_horario = models.TextField(blank=True, null=True)

    # Horas trabajadas por el chofer durante la semana (AUTOMATICO) (ARREGLAR DESPUES)
    horas_trabajadas_en_la_semana = models.IntegerField(default=0)

    # Número de clases canceladas (AUTOMATICO) (ARREGLAR DESPUES)
    clases_canceladas_en_la_semana = models.IntegerField(default=0)

    # Motivo de las inasistencias
    motivo_de_las_inasistencias = models.TextField(blank=True, null=True)

    # Fecha y hora en la que se registró esta asistencia (Timestamp)
    fecha_y_hora_en_la_que_se_registro_reporte = models.DateTimeField(auto_now_add=True)

    # Esto le cambiara el titulo a cada registro de la tabla

    def __str__(self):
        return f"{self.nombre_de_reporte_semanal}"

    class Meta:
        verbose_name_plural = "Reportes Semanales"


""" Modelo del Horario de los turnos del Lunes.

Los datos que necesito para el horario (o turno) son:
•	Nombre del turno (ej: turno de jesus - 02 ene - 10 am a 12 pm ). X
•	ID del chofer (tomado como clave foranea). X
•	ID de la oficina (tomada como clave foranea). X
•	ID del estudiante. X
•	Horario de inicio del turno. X
•	Horario de fin del turno. X
•	Semana del turno (tomado como clave foranea) X
•	Marca de tiempo. X

Sería buena idea agregarle una marca de tiempo a los turnos de los horarios, para saber cuando fue creado el horario. 
Sin embargo, no me dirá cuando fue la última modificación. Solo me dirá cuando fue agregado el horario.

Pero, como los secretarios pueden agregar horarios, la marca de tiempo puede ser útil, ya que me diría en qué fecha y a 
qué hora el secretario agregó tal horario.

Tengo que crear un campo que se llame “Fecha”, y solo agarraría la fecha (usando DateField). Dado que así lo ponía en 
el Excel el cliente, lo ideal sería agarrar la fecha de cada día. 

Pondre en todas las tablas de los horarios de todos los días si el Carro a usar es automático o sincrónico.
"""
class HorariosLunes(models.Model):

    # Esta es la lista donde se almacena si el carro es automático o sincrónico
    OPCIONES_AUTOMATICO_O_SINCRONICO = (
        ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
        ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    )

    # Nombre del horario (ej: "Horario de Pedro Perez")
    nombre_del_horario = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_del_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_lunes", default=0)

    # Oficina a la que le pertenece este horario
    id_de_oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
                                      related_name="oficina_a_la_que_le_pertenece_horario_lunes", default=0)

    # ID del estudiante
    id_del_estudiante = models.ForeignKey("Estudiante", on_delete=models.CASCADE, related_name="id_de_estudiante_lunes",
                                          default=0)

    # Hora de entrada y salida del turno
    hora_de_inicio_del_turno = models.TimeField(auto_now=False, auto_now_add=False)
    hora_de_fin_del_turno = models.TimeField(auto_now=False, auto_now_add=False)

    # Semana del turno
    semana_del_turno = models.ForeignKey("Semana", on_delete=models.CASCADE, related_name="semana_del_turno_del_lunes",
                                          default=0)

    # Esto guarda si el estudiante usará un carro sincrónico o automático
    usara_carro_automatico_o_sincronico = models.CharField(max_length=20, choices=OPCIONES_AUTOMATICO_O_SINCRONICO,
                                                           default='')

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(auto_now_add=True)

    # Timestamp erroneo
    # fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(default=date.today)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_del_horario}"

    class Meta:
        verbose_name_plural = "Horarios de los Lunes"


""" Modelo de los Horarios de los Martes

DEBO AGREGAR:
•	Semana del turno (tomado como clave foranea)
"""
class HorariosMartes(models.Model):
    OPCIONES_AUTOMATICO_O_SINCRONICO = (
        ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
        ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    )


    # Nombre del horario (ej: "Horario de Pedro Perez")
    nombre_del_horario = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_del_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_martes", default=0)

    # Oficina a la que le pertenece este horario
    id_de_oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
                                      related_name="oficina_a_la_que_le_pertenece_horario_martes", default=0)

    # ID del estudiante
    id_del_estudiante = models.ForeignKey("Estudiante", on_delete=models.CASCADE,
                                          related_name="id_de_estudiante_martes", default=0)

    # Hora de entrada y salida del turno
    hora_de_inicio_del_turno = models.TimeField(auto_now=False, auto_now_add=False)
    hora_de_fin_del_turno = models.TimeField(auto_now=False, auto_now_add=False)

    # Semana del turno
    semana_del_turno = models.ForeignKey("Semana", on_delete=models.CASCADE, related_name="semana_del_turno_del_martes",
                                          default=0)

    # Esto guarda si el estudiante usará un carro sincrónico o automático
    usara_carro_automatico_o_sincronico = models.CharField(max_length=20, choices=OPCIONES_AUTOMATICO_O_SINCRONICO,
                                                           default='')

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(auto_now_add=True)

    # fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(default=date.today)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_del_horario}"

    class Meta:
        verbose_name_plural = "Horarios de los Martes"


""" Modelo de los Horarios de los Miércoles.

DEBO AGREGAR:
•	Semana del turno (tomado como clave foranea)
"""
class HorariosMiercoles(models.Model):
    OPCIONES_AUTOMATICO_O_SINCRONICO = (
        ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
        ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    )

    # Nombre del horario (ej: "Horario de Pedro Perez")
    nombre_del_horario = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_del_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_miercoles",
                                      default=0)

    # Oficina a la que le pertenece este horario
    id_de_oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
                                      related_name="oficina_a_la_que_le_pertenece_horario_miercoles", default=0)

    # ID del estudiante
    id_del_estudiante = models.ForeignKey("Estudiante", on_delete=models.CASCADE,
                                          related_name="id_de_estudiante_miercoles", default=0)

    # Hora de entrada y salida del turno
    hora_de_inicio_del_turno = models.TimeField(auto_now=False, auto_now_add=False)
    hora_de_fin_del_turno = models.TimeField(auto_now=False, auto_now_add=False)

    # Semana del turno
    semana_del_turno = models.ForeignKey("Semana", on_delete=models.CASCADE,
                                         related_name="semana_del_turno_del_miercoles", default=0)

    # Esto guarda si el estudiante usará un carro sincrónico o automático
    usara_carro_automatico_o_sincronico = models.CharField(max_length=20, choices=OPCIONES_AUTOMATICO_O_SINCRONICO,
                                                           default='')

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(auto_now=True)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_del_horario}"

    class Meta:
        verbose_name_plural = "Horarios de los Miércoles"


""" Modelo de los Horarios de los Jueves.

DEBO AGREGAR:
•	Semana del turno (tomado como clave foranea)
"""
class HorariosJueves(models.Model):
    OPCIONES_AUTOMATICO_O_SINCRONICO = (
        ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
        ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    )

    # Nombre del horario (ej: "Horario de Pedro Perez")
    nombre_del_horario = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_del_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_jueves", default=0)

    # Oficina a la que le pertenece este horario
    id_de_oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
                                      related_name="oficina_a_la_que_le_pertenece_horario_jueves", default=0)

    # ID del estudiante
    id_del_estudiante = models.ForeignKey("Estudiante", on_delete=models.CASCADE,
                                          related_name="id_de_estudiante_jueves", default=0)

    # Hora de entrada y salida del turno
    hora_de_inicio_del_turno = models.TimeField(auto_now=False, auto_now_add=False)
    hora_de_fin_del_turno = models.TimeField(auto_now=False, auto_now_add=False)

    # Semana del turno
    semana_del_turno = models.ForeignKey("Semana", on_delete=models.CASCADE, related_name="semana_del_turno_del_jueves",
                                          default=0)

    # Esto guarda si el estudiante usará un carro sincrónico o automático
    usara_carro_automatico_o_sincronico = models.CharField(max_length=20, choices=OPCIONES_AUTOMATICO_O_SINCRONICO,
                                                           default='')

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(auto_now=True)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_del_horario}"

    class Meta:
        verbose_name_plural = "Horarios de los Jueves"


""" Modelo de los Horarios de los Viernes.

DEBO AGREGAR:
•	Semana del turno (tomado como clave foranea)
"""
class HorariosViernes(models.Model):
    OPCIONES_AUTOMATICO_O_SINCRONICO = (
        ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
        ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    )

    # Nombre del horario (ej: "Horario de Pedro Perez")
    nombre_del_horario = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_del_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_viernes",
                                      default=0)

    # Oficina a la que le pertenece este horario
    id_de_oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
                                      related_name="oficina_a_la_que_le_pertenece_horario_viernes", default=0)

    # ID del estudiante
    id_del_estudiante = models.ForeignKey("Estudiante", on_delete=models.CASCADE,
                                          related_name="id_de_estudiante_viernes", default=0)

    # Hora de entrada y salida del turno
    hora_de_inicio_del_turno = models.TimeField(auto_now=False, auto_now_add=False)
    hora_de_fin_del_turno = models.TimeField(auto_now=False, auto_now_add=False)

    # Semana del turno
    semana_del_turno = models.ForeignKey("Semana", on_delete=models.CASCADE,
                                         related_name="semana_del_turno_del_viernes", default=0)

    # Esto guarda si el estudiante usará un carro sincrónico o automático
    usara_carro_automatico_o_sincronico = models.CharField(max_length=20, choices=OPCIONES_AUTOMATICO_O_SINCRONICO,
                                                           default='')

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(auto_now=True)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_del_horario}"

    class Meta:
        verbose_name_plural = "Horarios de los Viernes"



""" Modelo de los Horarios de los Sabados.

DEBO AGREGAR:
•	Semana del turno (tomado como clave foranea) X
"""
class HorariosSabados(models.Model):
    OPCIONES_AUTOMATICO_O_SINCRONICO = (
        ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
        ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    )

    # Nombre del horario (ej: "Horario de Pedro Perez")
    nombre_del_horario = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_del_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_sabado", default=0)

    # Oficina a la que le pertenece este horario
    id_de_oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
                                      related_name="oficina_a_la_que_le_pertenece_horario_sabado", default=0)

    # ID del estudiante
    id_del_estudiante = models.ForeignKey("Estudiante", on_delete=models.CASCADE,
                                          related_name="id_de_estudiante_sabado", default=0)

    # Hora de entrada y salida del turno
    hora_de_inicio_del_turno = models.TimeField(auto_now=False, auto_now_add=False)
    hora_de_fin_del_turno = models.TimeField(auto_now=False, auto_now_add=False)

    # Semana del turno
    semana_del_turno = models.ForeignKey("Semana", on_delete=models.CASCADE, related_name="semana_del_turno_del_sabado",
                                          default=0)

    # Esto guarda si el estudiante usará un carro sincrónico o automático
    usara_carro_automatico_o_sincronico = models.CharField(max_length=20, choices=OPCIONES_AUTOMATICO_O_SINCRONICO,
                                                           default='')

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(auto_now=True)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_del_horario}"

    class Meta:
        verbose_name_plural = "Horarios de los Sábados"


""" Modelo de los Horarios de los Domingos.

"""
class HorariosDomingos(models.Model):
    OPCIONES_AUTOMATICO_O_SINCRONICO = (
        ('CARRO AUTOMATICO', 'CARRO AUTOMATICO'),
        ('CARRO SINCRONICO', 'CARRO SINCRONICO'),
    )

    # Nombre del horario (ej: "Horario de Pedro Perez")
    nombre_del_horario = models.CharField(max_length=255, default='')

    # ID del chofer (tomado como clave foranea)
    id_del_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer_domingo",
                                      default=0)

    # Oficina a la que le pertenece este horario
    id_de_oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
                                      related_name="oficina_a_la_que_le_pertenece_horario_domingo", default=0)

    # ID del estudiante
    id_del_estudiante = models.ForeignKey("Estudiante", on_delete=models.CASCADE,
                                          related_name="id_de_estudiante_domingo", default=0)

    # Hora de entrada y salida del turno
    hora_de_inicio_del_turno = models.TimeField(auto_now=False, auto_now_add=False)
    hora_de_fin_del_turno = models.TimeField(auto_now=False, auto_now_add=False)

    # Semana del turno
    semana_del_turno = models.ForeignKey("Semana", on_delete=models.CASCADE,
                                         related_name="semana_del_turno_del_domingo", default=0)

    # Esto guarda si el estudiante usará un carro sincrónico o automático
    usara_carro_automatico_o_sincronico = models.CharField(max_length=20, choices=OPCIONES_AUTOMATICO_O_SINCRONICO,
                                                           default='')

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(auto_now=True)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_del_horario}"

    class Meta:
        verbose_name_plural = "Horarios de los Domingos"

""" Modelo de Peticiones de cambiar horarios

En esta función, los secretarios podrán pedirle al adminsitrador que editen un horario, ya que los secretarios no 
podrán editar directamente los horarios. Si al administrador le parece bien modificar un horario, él modificará el 
horario. Sino, el administrador ignorará la petición, y el horario no se modificará

	Los datos que necesito para las peticiones son:

•	Nombre del chofer y del turno que deseas modificar. X
•	Nombre del chofer al que le deseas cambiar el horario. X
•	Nuevo horario de inicio del turno. X
•	Nuevo Horario de fin del turno. X
•	Nueva oficina que le deseas agregar al turno. X
•	Nuevo estudiante que le deseas agregar al turno. X
•	Día de la semana (Lunes, Martes, etc) (ESCOGER DE UNA LISTA). X
•	Nuevo nombre que le deseas agregar al turno (ej: turno de jesus - 02 ene - 10 am a 12 pm ). X
•	Semana del turno (tomado como clave foranea) X
•	Timestamp o Marca de Tiempo. X 

En principio, no voy a editar el chofer.

voy a llamarle "nombre y fecha y hora del horario a cambiar" al campo que debe llenar el secretario para decir cual 
turno quiere modificar. No puedo poner "nombre, fecha y hora" porque no puedo colocar "," en el nombre de unc campo, 
porque la bbdd no lo detecta.

Ahora que lo pienso, sería buena idea saber quien es el chofer al que le quiero modificar el horario. Entonces, pondré 
la ID del chofer al que le deseo dar el horario. 

Además, sería buena idea cambiar el campo del nombre del horario anterior a “nombre DEL CHOFER y fecha y hora” al que 
se le desea cambiar el horario.
"""
class PeticionParaCambiarHorario(models.Model):

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

    # Nombre, fecha y hora del turno que deseas modificar
    nombre_del_chofer_y_fecha_y_hora_del_horario_que_deseas_modificar = models.CharField(max_length=255, default='')

    # ID del chofer del horario que quieres modificar (tomado como clave foranea)
    id_del_chofer_del_horario_a_modificar = models.ForeignKey("Chofer", on_delete=models.CASCADE,
                                    related_name="chofer_horario_a_modificar",
                                    default=0)

    # Nueva Hora de entrada y salida para el turno
    hora_de_inicio_del_nuevo_turno = models.TimeField(auto_now=False, auto_now_add=False)
    hora_de_fin_del_nuevo_turno = models.TimeField(auto_now=False, auto_now_add=False)

    # Nueva Oficina a la que le deseas asignar al nuevo horario
    id_de_oficina_para_nuevo_horario = models.ForeignKey("Oficina", on_delete=models.CASCADE,
                                      related_name="oficina_para_el_nuevo_horario", default=0)

    # ID del Nuevo Estudiante al que le deseas asignar este turno
    id_de_estudiante_para_nuevo_horario = models.ForeignKey("Estudiante", on_delete=models.CASCADE,
                                          related_name="id_de_estudiante_para_nuevo_horario", default=0)

    # Día de la semana a la que le deseas asignar a este turno
    dia_de_la_semana_para_el_nuevo_horario = models.CharField(max_length=20, choices=OPCIONES_DIAS_DE_LA_SEMANA)

    # Nuevo Nombre para el horario (ej: "Horario de Pedro Perez")
    nombre_para_el_nuevo_horario = models.CharField(max_length=255, default='')

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_turno = models.DateTimeField(auto_now=True)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_del_chofer_y_fecha_y_hora_del_horario_que_deseas_modificar}"

    class Meta:
        verbose_name_plural = "Peticiones Para Cambiar Horarios"


""" Modelo de Semanas.

Tengo que crear un campo que se llame “Fecha”, y solo agarraría la fecha (usando DateField). Dado que así lo ponía en 
el Excel el cliente, lo ideal sería agarrar la fecha de cada día. 

Los datos que debe contener cada semana son:
•	Nombre de la semana. X
•	Fecha del lunes. X
•	Fecha del martes. X
•	Fecha del miércoles. X
•	Fecha del jueves. X
•	Fecha del viernes. X
•	Fecha del sábado. X
•	Marca de tiempo. X
"""
class Semana(models.Model):

    # Nombre, fecha y hora del turno que deseas modificar
    nombre_de_la_semana = models.CharField(max_length=255, default='')

    # Fecha del lunes de esa semana
    fecha_del_lunes = models.DateField(default=date.today)

    # Martes
    fecha_del_martes = models.DateField(default=date.today)

    # Miercoles
    fecha_del_miercoles = models.DateField(default=date.today)

    # Jueves
    fecha_del_jueves = models.DateField(default=date.today)

    # Viernes
    fecha_del_viernes = models.DateField(default=date.today)

    # Sabado
    fecha_del_sabado = models.DateField(default=date.today)

    # Domingo
    fecha_del_domingo = models.DateField(default=date.today)

    # Fecha y hora en la que se registró este turno (Timestamp)
    fecha_y_hora_en_la_que_se_registro_semana = models.DateTimeField(auto_now=True)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_de_la_semana}"


""" Modelo de Semanas para Reportes Semanales.

Este es un modelo redundante en el que se almacenarán las semanas en las que se crearán los reportes semanales (es
decir, cada semana para cada reporte se almacenará aquí).

Hay un montón de problemas que podrían surgir si limito el número de tablas de semanas que el chofer puede ver en su 
propio horario. Por ejemplo, si los 5 nuevos horarios de las 5 semanas no tienen ningun horario, el chofer no veria 
cual eran sus clases anteriores. Solución: crear una tabla redundante que almacene las semanas para los reportes 
semanales.

Los datos que pondré en la tabla de Semanas de Reporte Semanal serán:
•	Nombre (de que fecha a que fecha es). X
•	Fecha de inicio de esa semana. X
•	Fecha de fin de esa semana. X

Solo sería eso. No necesitaría más nada. Pondré la fecha de inicio y la fecha de fin para imprimirlos en la tabla en el 
formato dia/mes/año, aunque el usuario ponga lo que le de la gana en “Nombre” y escriba algo mal.
"""
class SemanaParaReportesSemanales(models.Model):

    # Nombre de la semana a evaluar
    nombre_de_la_semana = models.CharField(max_length=255, default='')

    # Fecha de inicio de la semana a evaluar
    fecha_de_inicio_de_semana_a_evaluar = models.DateField(default=date.today)

    # Fecha del final de la semana a evaluar
    fecha_final_de_semana_a_evaluar = models.DateField(default=date.today)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.nombre_de_la_semana}"

    class Meta:
        verbose_name_plural = "Semanas Para Reportes Semanales"







# """ Modelo de Horarios.
#
# Los datos que pondré en la tabla de horarios son:
# •	ID del chofer (tomado como clave foránea de la tabla de Chofer)
# •	Oficina a la que le pertenece este horario
# •	Horario de inicio Lunes (obligatorio).
# •	Horario de Fin Lunes (obligatorio).
# •	Horario de Inicio de Segundo Turno Lunes (opcional).
# •	Horario de Fin de Segundo Turno Lunes (opcional).
# •	Horario de inicio Martes
# •	Horario de Fin Martes
# •	Horario de Inicio de Segundo Turno Martes
# •	Horario de Fin de Segundo Turno Martes
# •	Horario de inicio Miercoles
# •	Horario de Fin Miercoles
# •	Horario de Inicio de Segundo Turno Miercoles
# •	Horario de Fin de Segundo Turno Miercoles
# •	Horario de inicio Jueves
# •	Horario de Fin Jueves
# •	Horario de Inicio de Segundo Turno Jueves
# •	Horario de Fin de Segundo Turno Jueves
# •	Horario de inicio Viernes
# •	Horario de Fin Viernes
# •	Horario de Inicio de Segundo Turno Viernes
# •	Horario de Fin de Segundo Turno Viernes
# •	Horario de inicio Sabado
# •	Horario de Fin Sabado
# •	Horario de Inicio de Segundo Turno Sabado
# •	Horario de Fin de Segundo Turno Sabado
# •	Horario de inicio Domingo
# •	Horario de Fin Domingo
# •	Horario de Inicio de Segundo Turno Domingo
# •	Horario de Fin de Segundo Turno Domingo
#
#     Pondré 2 horarios por cada día por si un profesor trabaja a "turno partido", es decir, si el profesor trabaja
# en la mañana, luego descansa, y leugo tiene que venir en la tarde a terminar su turno.
#
#     Todos los campos con el nombre "segundo turno" son opcionales.
#
#     Si hay días en los que no hay clase (ejemplo: los fines de semana) pondré que el usuario deba poner 0:00 o algo así.
# Otra forma de arreglarlo sería que el campo fuera “Varchar” para que el usuario insertara texto (para que insertara
# algo como “N/A”). Sin embargo, por motivos de foolproofing, prefiero no hacer eso. ¿Por qué? Porque si pongo que el
# usuario ponga texto, puede ser que escriba “1:00 pm”, o “13:00”, o “1 pm”, o “a la una”, y eso me va a dar un monton de
# problemas al largo plazo. Mientras tanto, si lo dejo com “timeField”, el usuario solo podrá escribir números.
#
# “Blank = true” significa que, si estuviera en un formulario, que está permitido que ese campo en el formulario del
# front end de la web app estuviera vacio. Sin embargo, lo que yo quería, es decir, que el campo pueda ser NULL, requiere
# que ponga ewl atributo “Null=true”.
#
# Tengo que agregar “f{self.columna}” dentro de un “def __str__(self)” para cambiarle el nombre al título de los campos
# de una tabla en la bbdd en Django.
#
# Va a haber una relación de uno a muchos entre los horarios y las oficinas, ya que un horario en
# específico solo puede pertenecer a una oficina, pero una oficina puede tener muchos horarios asociados a ella.
# Entonces, hay una relación one-to-many entre oficinas y horarios. El one-to-many se hace usando claves foráneas.
# Por lo tanto, agarraré los horarios usando una clave foránea.
#
# Sin embargo, el horario lo debo agarrar desde la tabla de horarios, NO desde la tabla de oficinas. Cada horario
# solo pertenece a una oficina. Por lo tanto, al crear un registro de un horario, también debo poder seleccionar
# la oficina a la que le pertenece ese horario.
#
# Tengo que poner "default=0" en la clave foránea que agarra la oficina, porque mínimo se debe tener un número
# por defecto al crear una tabla que use una clave foránea.
#
# Creo que preferiría asignarle un nombre a los horarios, para así encontrarlos más fácilmente. No voy a dejar el nombre
# de usuario como el nombre de usuario, porque el usuario “pedro” podría ser “Pedro Gonzales” o “Pedro Perez”, pero
# “Horario de Pedro Pérez” es mucho más específico y me dice el nombre de la persona exacta.
#
# Voy a hacer que todos los horarios de todos los días sean opcionales (es decir, que puedan ser NULL). Eso es porque,
# primero que nada, hay posiblemente quienes no trabajen los fines de semana. Además, si alguien trabaja los sabados,
# pero no trabaja los lunes, entonces no debería salir nada en “lunes”. Finalmente, como no puedo poner “N/A” al horario
# de un dia en el que un chofer no venga a trabajar, me sale mejor dejar esos días como un campo vacío. Entonces, dejaré
# todos los días como opcionales (Null=True).
#
# O, después de pensarlo mejor, dado a que los estudiantes solo les interesan los horarios de los choferes, y no de los
# secretarios ni administradores, , en el modelo de Horarios, solo le dejare al usuario seleccionar choferes, NO a todos
# los usuarios. Y lo mismo con las oficinas: solo se podrán asignar choferes a las oficinas, NO secretarios ni
# administradores.
# """
#
#
# class Horario(models.Model):
#     # Nombre del horario (ej: "Horario de Pedro Perez")
#     nombre_del_horario = models.CharField(max_length=255, default='')
#
#     # ID del chofer (tomado como clave foranea)
#     id_de_chofer = models.ForeignKey("Chofer", on_delete=models.CASCADE, related_name="id_de_chofer", default=0)
#
#     # Oficina a la que le pertenece este horario
#     oficina = models.ForeignKey("Oficina", on_delete=models.CASCADE,
#                                 related_name="oficina_a_la_que_le_pertenece_este_horario", default=0)
#
#     # Horarios iniciales de entrada y salida los lunes (obligatorio)
#     horario_de_inicio_lunes = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
#     horario_de_fin_lunes = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
#
#     # Segundos horarios de entrada y salida los lunes (opcional)
#     horario_de_inicio_segundo_turno_lunes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_segundo_turno_lunes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#
#     # Martes
#     horario_de_inicio_martes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_martes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_inicio_segundo_turno_martes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_segundo_turno_martes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#
#     # Miércoles
#     horario_de_inicio_miercoles = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_miercoles = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_inicio_segundo_turno_miercoles = models.TimeField(blank=True, auto_now=False, auto_now_add=False,
#                                                                  null=True)
#     horario_de_fin_segundo_turno_miercoles = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#
#     # Jueves
#     horario_de_inicio_jueves = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_jueves = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_inicio_segundo_turno_jueves = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_segundo_turno_jueves = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#
#     # Viernes
#     horario_de_inicio_viernes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_viernes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_inicio_segundo_turno_viernes = models.TimeField(blank=True, auto_now=False, auto_now_add=False,
#                                                                null=True)
#     horario_de_fin_segundo_turno_viernes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#
#     # Sábado
#     horario_de_inicio_sabado = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_sabado = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_inicio_segundo_turno_sabado = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_segundo_turno_sabado = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#
#     # Domingo
#     horario_de_inicio_domingo = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_fin_domingo = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#     horario_de_inicio_segundo_turno_domingo = models.TimeField(blank=True, auto_now=False, auto_now_add=False,
#                                                                null=True)
#     horario_de_fin_segundo_turno_domingo = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
#
#     # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
#     def __str__(self):
#         return f"{self.nombre_del_horario}"
