""" El "urlpatterns" me permitirá acceder a cada template o pagina a través de las distintas URLs (fuente:
https://youtu.be/pRNhdI9PVmg) .

Dado a que cada semana tiene una lsita de reportes distinta, es decir, que voy a tener que generar un monton de páginas
de manera dinámica, tendré que agregar la ID de la semana seleccionada a la URL de la página con la lista de reportes
semanales.
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
    path('lista-reportes-semanales/<str:semana_id>', views.lista_reportes_semanales_semana_seleccionada,
         name='lista_reportes_semanales_semana_seleccionada'),
    path('reporte-semanal/<str:reporte_id>', views.reporte_semanal,
         name='reporte_semanal'),

    # URLs a Páginas de Horarios para secretarios
    path('agregar-horarios', views.agregar_horarios, name='agregar_horarios'),
    path('todos-los-horarios', views.horarios_de_todos_los_choferes, name='horarios_de_todos_los_choferes'),



    # Mensaje de error
    path('error', views.mensaje_de_error, name='mensaje_de_error'),

]
