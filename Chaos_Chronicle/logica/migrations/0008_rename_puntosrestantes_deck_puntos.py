# Generated by Django 5.0.4 on 2024-06-05 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logica', '0007_remove_carta_tipo_remove_deck_cartas_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deck',
            old_name='PuntosRestantes',
            new_name='Puntos',
        ),
    ]