# Generated by Django 4.1.4 on 2023-01-09 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0032_horariosjueves_semana_del_turno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peticionparacambiarhorario',
            name='dia_de_la_semana_para_el_nuevo_horario',
            field=models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=20),
        ),
        migrations.CreateModel(
            name='HorariosDomingos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_del_horario', models.CharField(default='', max_length=255)),
                ('hora_de_inicio_del_turno', models.TimeField()),
                ('hora_de_fin_del_turno', models.TimeField()),
                ('fecha_y_hora_en_la_que_se_registro_turno', models.DateTimeField(auto_now=True)),
                ('id_de_oficina', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='oficina_a_la_que_le_pertenece_horario_domingo', to='app_horarios.oficina')),
                ('id_del_chofer', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='id_de_chofer_domingo', to='app_horarios.chofer')),
                ('id_del_estudiante', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='id_de_estudiante_domingo', to='app_horarios.estudiante')),
                ('semana_del_turno', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='semana_del_turno_del_domingo', to='app_horarios.semana')),
            ],
        ),
    ]