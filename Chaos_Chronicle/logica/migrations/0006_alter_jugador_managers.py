# Generated by Django 5.0.4 on 2024-05-31 22:04

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logica', '0005_alter_jugador_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='jugador',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
