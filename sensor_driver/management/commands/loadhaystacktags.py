import csv
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from sensor_driver.models import HaystackTag

class Command(BaseCommand):
    help = 'Load data from a CSV file into HaystackTag model'

    def handle(self, *args, **options):
        # Lista de URLs a procesar
        urls = [
            ['https://project-haystack.org/doc/appendix/protocol', 'protocol'],
            ['https://project-haystack.org/doc/appendix/quantity', 'quantity'],
            ['https://project-haystack.org/doc/appendix/space', 'space'],
            ['https://project-haystack.org/doc/appendix/equip', 'equip'],
            ['https://project-haystack.org/doc/appendix/device', 'device']
        ]
        
        # Crear un archivo CSV para guardar los datos
        csv_filename = 'datos-haystack.csv'
        csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        
        # Iterar a través de las URLs y recopilar los datos en el CSV
        for url, categoria in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        
            table = soup.find('table')
            for index, row in enumerate(table.find_all('tr')):
                if index == 0:  # Saltar la primera fila
                    continue
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    id = th.text.strip()
                    descripcion = td.text.strip()
                    estado = 'I' if categoria == 'protocol' and id not in ['coap', 'http', 'modbus', 'mqtt'] else 'A'
                    csv_writer.writerow([id, descripcion, categoria, estado])

        # Obtener los datos de la URL de zona horaria
        tz_url = 'https://project-haystack.org/download/tz.txt'
        tz_response = requests.get(tz_url)
        tz_data = tz_response.text.strip().split('\n')

        # Agregar los datos al archivo CSV
        for tz_id in tz_data:
            csv_writer.writerow([tz_id, tz_id, 'timezone', 'A'])
        
        # Cerrar el archivo CSV
        csv_file.close()
        
        # Cargar datos desde el CSV al modelo HaystackTag
        with open(csv_filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row) >= 2:
                    haystack_tag_id = row[0]
                    haystack_tag_name = row[1]
                    haystack_tag_category = row[2]
                    haystack_tag_state = row[3]
                    try:
                        HaystackTag.objects.create(id=haystack_tag_id, name=haystack_tag_name,
                                                   category=haystack_tag_category, state=haystack_tag_state)
                        self.stdout.write(self.style.SUCCESS(f'Successfully created HaystackTag with id {haystack_tag_id}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error creating HaystackTag: {e}'))
                else:
                    self.stdout.write(self.style.WARNING('Incomplete row in CSV, skipping...'))
        
        self.stdout.write(self.style.SUCCESS(f'Data loaded from CSV to HaystackTag model'))
