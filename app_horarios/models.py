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

"""
class Chofer(models.Model):

    # ID del chofer (tomado como clave foranea)
    id_de_usuario = models.ForeignKey("User", on_delete=models.CASCADE, related_name="id_de_usuario_de_chofer")

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True, max_length=20)
    email = models.EmailField(blank=True, null=True, max_length=254)


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
"""
class Secretario(models.Model):

    # ID del chofer (tomado como clave foranea)
    id_de_usuario = models.ForeignKey("User", on_delete=models.CASCADE, related_name="id_de_usuario_de_secretario")

    # Si el usuario es secretario (SIEMPRE DEJARLO EN "True")
    el_usuario_es_secretario = models.BooleanField(default=True)


""" Modelo de Horarios.

Los datos que pondré en la tabla de horarios son:
•	ID del chofer (tomado como clave foránea de la tabla de Chofer)
•	Horario de inicio Lunes (obligatorio).
•	Horario de Fin Lunes (obligatorio).
•	Horario de Inicio de Segundo Turno Lunes (opcional).
•	Horario de Fin de Segundo Turno Lunes (opcional).
•	Horario de inicio Martes
•	Horario de Fin Martes
•	Horario de Inicio de Segundo Turno Martes
•	Horario de Fin de Segundo Turno Martes
•	Horario de inicio Miercoles
•	Horario de Fin Miercoles
•	Horario de Inicio de Segundo Turno Miercoles
•	Horario de Fin de Segundo Turno Miercoles
•	Horario de inicio Jueves
•	Horario de Fin Jueves
•	Horario de Inicio de Segundo Turno Jueves
•	Horario de Fin de Segundo Turno Jueves
•	Horario de inicio Viernes
•	Horario de Fin Viernes
•	Horario de Inicio de Segundo Turno Viernes
•	Horario de Fin de Segundo Turno Viernes
•	Horario de inicio Sabado
•	Horario de Fin Sabado
•	Horario de Inicio de Segundo Turno Sabado
•	Horario de Fin de Segundo Turno Sabado
•	Horario de inicio Domingo
•	Horario de Fin Domingo
•	Horario de Inicio de Segundo Turno Domingo
•	Horario de Fin de Segundo Turno Domingo

    Pondré 2 horarios por cada día por si un profesor trabaja a "turno partido", es decir, si el profesor trabaja
en la mañana, luego descansa, y leugo tiene que venir en la tarde a terminar su turno.

    Todos los campos con el nombre "segundo turno" son opcionales.
    
    Si hay días en los que no hay clase (ejemplo: los fines de semana) pondré que el usuario deba poner 0:00 o algo así. 
Otra forma de arreglarlo sería que el campo fuera “Varchar” para que el usuario insertara texto (para que insertara 
algo como “N/A”). Sin embargo, por motivos de foolproofing, prefiero no hacer eso. ¿Por qué? Porque si pongo que el 
usuario ponga texto, puede ser que escriba “1:00 pm”, o “13:00”, o “1 pm”, o “a la una”, y eso me va a dar un monton de 
problemas al largo plazo. Mientras tanto, si lo dejo com “timeField”, el usuario solo podrá escribir números.

“Blank = true” significa que, si estuviera en un formulario, que está permitido que ese campo en el formulario del 
front end de la web app estuviera vacio. Sin embargo, lo que yo quería, es decir, que el campo pueda ser NULL, requiere 
que ponga ewl atributo “Null=true”.

Tengo que agregar “f{self.columna}” dentro de un “def __str__(self)” para cambiarle el nombre al título de los campos 
de una tabla en la bbdd en Django.
"""
class Horario(models.Model):

    # ID del chofer (tomado como clave foranea)
    id_de_usuario = models.ForeignKey("User", on_delete=models.CASCADE, related_name="id_de_chofer")

    # Horarios iniciales de entrada y salida los lunes (obligatorio)
    horario_de_inicio_lunes = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_fin_lunes = models.TimeField(auto_now=False, auto_now_add=False)

    # Segundos horarios de entrada y salida los lunes (opcional)
    horario_de_inicio_segundo_turno_lunes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
    horario_de_fin_segundo_turno_lunes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)

    # Martes
    horario_de_inicio_martes = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_fin_martes = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_inicio_segundo_turno_martes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
    horario_de_fin_segundo_turno_martes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)

    # Miércoles
    horario_de_inicio_miercoles = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_fin_miercoles = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_inicio_segundo_turno_miercoles = models.TimeField(blank=True, auto_now=False, auto_now_add=False,
                                                                 null=True)
    horario_de_fin_segundo_turno_miercoles = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)

    # Jueves
    horario_de_inicio_jueves = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_fin_jueves = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_inicio_segundo_turno_jueves = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
    horario_de_fin_segundo_turno_jueves = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)

    # Viernes
    horario_de_inicio_viernes = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_fin_viernes = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_inicio_segundo_turno_viernes = models.TimeField(blank=True, auto_now=False, auto_now_add=False,
                                                               null=True)
    horario_de_fin_segundo_turno_viernes = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)

    # Sábado
    horario_de_inicio_sabado = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_fin_sabado = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_inicio_segundo_turno_sabado = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)
    horario_de_fin_segundo_turno_sabado = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)

    # Domingo
    horario_de_inicio_domingo = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_fin_domingo = models.TimeField(auto_now=False, auto_now_add=False)
    horario_de_inicio_segundo_turno_domingo = models.TimeField(blank=True, auto_now=False, auto_now_add=False,
                                                               null=True)
    horario_de_fin_segundo_turno_domingo = models.TimeField(blank=True, auto_now=False, auto_now_add=False, null=True)

    # Esto le cambiara el titulo a cada registro de la tabla para que aparezca el nombre del chofer en el horario
    def __str__(self):
        return f"{self.id_de_usuario}"


