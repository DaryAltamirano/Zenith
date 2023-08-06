import csv
from django.core.management.base import BaseCommand
from sensor_driver.models import HaystackTag

class Command(BaseCommand):
    help = 'Load data from a CSV file into HaystackTag model'

    def handle(self, *args, **options):
        csv_file = 'sensor_driver/datos-haystack.csv'  
        with open(csv_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile) 
            for row in csvreader:
                if len(row) >= 2:
                    haystack_tag_id = row[0]
                    haystack_tag_name = row[1]
                    try:
                        HaystackTag.objects.create(id=haystack_tag_id, name=haystack_tag_name)
                        self.stdout.write(self.style.SUCCESS(f'Successfully created HaystackTag with id {haystack_tag_id}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error creating HaystackTag: {e}'))
                else:
                    self.stdout.write(self.style.WARNING('Incomplete row in CSV, skipping...'))
