# Generated by Django 4.1.4 on 2023-01-02 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0004_alter_horario_horario_de_fin_segundo_turno_lunes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_segundo_turno_domingo',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_segundo_turno_jueves',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_segundo_turno_martes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_segundo_turno_miercoles',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_segundo_turno_sabado',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_segundo_turno_viernes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_segundo_turno_domingo',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_segundo_turno_jueves',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_segundo_turno_martes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_segundo_turno_miercoles',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_segundo_turno_sabado',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_segundo_turno_viernes',
            field=models.TimeField(blank=True, null=True),
        ),
    ]