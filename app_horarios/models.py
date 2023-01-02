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
    direccion = models.TextField(blank=True)
    telefono = models.CharField(blank=True, max_length=20)
    email = models.EmailField(blank=True, max_length=254)


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
