# Generated by Django 4.1.4 on 2023-01-03 16:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0013_asistencia_id_de_chofer'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='fecha',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='fecha_y_hora_en_la_que_se_registro_asistencia',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='horas_trabajadas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='vino_a_trabajar',
            field=models.CharField(choices=[('Sí', 'Sí'), ('No', 'No')], default='Sí', max_length=2),
        ),
    ]