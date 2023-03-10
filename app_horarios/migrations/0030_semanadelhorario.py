# Generated by Django 4.1.4 on 2023-01-09 12:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0029_rename_nombre_y_fecha_y_hora_del_horario_que_deseas_modificar_peticionparacambiarhorario_nombre_del_'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemanaDelHorario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_la_semana', models.CharField(default='', max_length=255)),
                ('fecha_del_lunes', models.DateField(default=datetime.date.today)),
                ('fecha_del_martes', models.DateField(default=datetime.date.today)),
                ('fecha_del_miercoles', models.DateField(default=datetime.date.today)),
                ('fecha_del_jueves', models.DateField(default=datetime.date.today)),
                ('fecha_del_viernes', models.DateField(default=datetime.date.today)),
                ('fecha_del_sabado', models.DateField(default=datetime.date.today)),
                ('fecha_y_hora_en_la_que_se_registro_semana', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
