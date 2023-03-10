# Generated by Django 4.1.4 on 2023-01-02 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_horarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Secretario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('el_usuario_es_secretario', models.BooleanField(default=True)),
                ('id_de_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_de_usuario_de_secretario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
