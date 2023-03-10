# Generated by Django 4.1.4 on 2023-01-08 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0027_horariosjueves_fecha_y_hora_en_la_que_se_registro_turno_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeticionParaCambiarHorario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_y_fecha_y_hora_del_horario_que_deseas_modificar', models.CharField(default='', max_length=255)),
                ('hora_de_inicio_del_nuevo_turno', models.TimeField()),
                ('hora_de_fin_del_nuevo_turno', models.TimeField()),
                ('dia_de_la_semana_para_el_nuevo_horario', models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado')], max_length=20)),
                ('nombre_para_el_nuevo_horario', models.CharField(default='', max_length=255)),
                ('fecha_y_hora_en_la_que_se_registro_turno', models.DateTimeField(auto_now=True)),
                ('id_de_estudiante_para_nuevo_horario', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='id_de_estudiante_para_nuevo_horario', to='app_horarios.estudiante')),
                ('id_de_oficina_para_nuevo_horario', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='oficina_para_el_nuevo_horario', to='app_horarios.oficina')),
            ],
        ),
    ]
