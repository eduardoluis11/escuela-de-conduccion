# Generated by Django 4.1.4 on 2023-01-08 12:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0021_alter_horarioslunes_id_de_oficina_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='horarioslunes',
            name='fecha_y_hora_en_la_que_se_registro_turno',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]