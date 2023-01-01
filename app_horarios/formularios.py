# Esto me deja usar los formularios de Django
from django import forms

# Esto me dejará agarrar fecha la fecha de hoy
from datetime import date

""" Formulario de Inicio de Sesión.

La contraseña tiene un widget que censurará la contrasela por motivos de seguridad.

Para evitar problemas con la base de datos, tengo que escribir "contrasena", no "contraseña".
"""
class FormularioInicioSesion(forms.Form):
    nombre_de_usuario = forms.CharField(max_length=100)
    contrasena = forms.CharField(max_length=2000, widget=forms.PasswordInput)   # Contraseña