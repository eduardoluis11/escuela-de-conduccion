from django.contrib import admin

# Esto importará todos los modelos que he creado
from .models import User, Chofer, Secretario, Horario, Oficina, Asistencia

# Registra tus modelos aquí

# Esto registra cada modelo de models.py. Deberia ponermelo visible en el panel de admin de Django
admin.site.register(User)
admin.site.register(Chofer)
admin.site.register(Secretario)
admin.site.register(Horario)
admin.site.register(Oficina)
admin.site.register(Asistencia)
