from django.contrib import admin

# Esto importará todos los modelos que he creado
from .models import User, Chofer, Secretario, Oficina, Asistencia, ReporteSemanal, Estudiante, HorariosLunes, \
    HorariosMartes, HorariosMiercoles, HorariosJueves, HorariosViernes, HorariosSabados, HorariosDomingos, \
    PeticionParaCambiarHorario, Semana, SemanaParaReportesSemanales


# Esto agrega una función de búsqueda en el panel de admin de Django por nombre
class CustomModelAdmin(admin.ModelAdmin):
    search_fields = ['nombre']  # Agrega los campos por los que deseas buscar


# Registra tus modelos aquí

# Esto registra cada modelo de models.py. Deberia ponermelo visible en el panel de admin de Django
admin.site.register(User)

# Los choferes se podrán buscar por nombre en el panel de admin de Django
admin.site.register(Chofer, CustomModelAdmin)

admin.site.register(Secretario)
admin.site.register(Oficina)
admin.site.register(Asistencia)
admin.site.register(ReporteSemanal)
admin.site.register(Estudiante)
admin.site.register(HorariosLunes)
admin.site.register(HorariosMartes)
admin.site.register(HorariosMiercoles)
admin.site.register(HorariosJueves)
admin.site.register(HorariosViernes)
admin.site.register(HorariosSabados)
admin.site.register(HorariosDomingos)
admin.site.register(PeticionParaCambiarHorario)
admin.site.register(Semana)
admin.site.register(SemanaParaReportesSemanales)



