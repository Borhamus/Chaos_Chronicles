# main/management/commands/load_cartas.py

import os
import csv
from django.core.management.base import BaseCommand
from logica.models import Carta

class Command(BaseCommand):
    help = 'Load cartas from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('File "%s" does not exist' % file_path))
            return

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                carta = Carta(
                    Nombre=row['Nombre'],
                    Costo=row['Costo'],
                    Ataque=row['Ataque'],
                    Defensa=row['Defensa']
                    # Imagen puede ser asignada aquí si la URL o el path de la imagen está en el archivo TXT
                )
                carta.save()
                self.stdout.write(self.style.SUCCESS('Carta "%s" loaded' % row['Nombre']))

