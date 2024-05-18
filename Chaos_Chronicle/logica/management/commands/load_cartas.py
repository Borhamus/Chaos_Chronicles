# load_cartas.py

import os
import csv
from django.core.management.base import BaseCommand
from logica.models import Carta

class Command(BaseCommand):
    help = 'Load cartas from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the CSV file')
        parser.add_argument('images_path', type=str, help='The path to the images directory')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        images_path = kwargs['images_path']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File "{file_path}" does not exist'))
            return

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                image_filename = os.path.join(images_path, row['Nombre'] + '.jpg')
                if os.path.exists(image_filename):
                    carta = Carta(
                        Nombre=row['Nombre'],
                        Costo=row['Costo'],
                        Ataque=row['Ataque'],
                        Defensa=row['Defensa'],
                        Imagen=image_filename  # Ajusta esto según sea necesario
                    )
                    carta.save()
                    self.stdout.write(self.style.SUCCESS(f'Carta "{row["Nombre"]}" loaded with image'))
                else:
                    self.stdout.write(self.style.WARNING(f'Image for carta "{row["Nombre"]}" not found'))
