# Generated by Django 4.1.4 on 2023-01-09 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0033_alter_peticionparacambiarhorario_dia_de_la_semana_para_el_nuevo_horario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='semana',
            name='fecha_del_domingo',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
