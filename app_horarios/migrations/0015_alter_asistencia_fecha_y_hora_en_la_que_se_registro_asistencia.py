# Generated by Django 4.1.4 on 2023-01-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0014_asistencia_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistencia',
            name='fecha_y_hora_en_la_que_se_registro_asistencia',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]