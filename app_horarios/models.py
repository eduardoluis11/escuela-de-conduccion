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

