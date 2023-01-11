""" El "urlpatterns" me permitirá acceder a cada template o pagina a través de las distintas URLs (fuente:
https://youtu.be/pRNhdI9PVmg) .

"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('iniciar-sesion', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('horario-chofer', views.horario_chofer_logueado, name='horario_chofer_logueado'),

    # URLs a Páginas con Reportes Semanales
    path('lista-fechas-con-reportes-semanales', views.lista_fechas_reportes_semanales,
         name='lista_fechas_reportes_semanales'),
    path('lista-reportes-semanales', views.lista_reportes_semanales_semana_seleccionada,
         name='lista_reportes_semanales_semana_seleccionada'),
]
