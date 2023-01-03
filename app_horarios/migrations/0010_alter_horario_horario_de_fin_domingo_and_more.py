# Generated by Django 4.1.4 on 2023-01-03 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0009_horario_nombre_del_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_domingo',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_jueves',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_lunes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_martes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_miercoles',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_sabado',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_viernes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_domingo',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_jueves',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_lunes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_martes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_miercoles',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_sabado',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_viernes',
            field=models.TimeField(blank=True, null=True),
        ),
    ]