# Generated by Django 4.1.4 on 2023-01-02 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0003_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='horario_de_fin_segundo_turno_lunes',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='horario_de_inicio_segundo_turno_lunes',
            field=models.TimeField(blank=True, null=True),
        ),
    ]