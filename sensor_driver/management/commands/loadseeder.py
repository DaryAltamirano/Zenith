import random
import csv
from django.core.management.base import BaseCommand
from sensor_driver.models import Zone, Space, Equip, Sensor

class Command(BaseCommand):
    help = 'Load mock data into the database' 

    def handle(self, *args, **kwargs):
        zone_csv_file = '/code/static/docs/zone.csv'
        equip_csv_file = '/code/static/docs/equip.csv'
        space_csv_file = '/code/static/docs/space.csv'
        sensor_csv_file = '/code/static/docs/sensor.csv'

        # Load Zone data
        with open(zone_csv_file, 'r') as zone_file:
            zone_csv_reader = csv.reader(zone_file)
            for zone_row in zone_csv_reader:
                Zone.objects.create(
                    name=zone_row[1],
                    geoAddr=zone_row[2],
                    geoCoord=zone_row[3],
                    tz=zone_row[4],
                )

        all_zones = Zone.objects.all()

        with open(space_csv_file, 'r') as space_file:
            space_csv_reader = csv.reader(space_file)
            for space_row in space_csv_reader:
                random_zone = random.choice(all_zones)
                Space.objects.create(
                    spaceref=space_row[1],
                    name=space_row[2],
                    area=space_row[3],
                    zone=random_zone,
                )

        with open(equip_csv_file, 'r') as equip_file:
            equip_csv_reader = csv.reader(equip_file)
            for equip_row in equip_csv_reader:
                random_space = random.choice(Space.objects.filter(zone=random_zone))
                Equip.objects.create(
                    name=equip_row[1],
                    equipref=equip_row[2],
                    space=random_space,
                )

        with open(sensor_csv_file, 'r') as sensor_file:
            sensor_csv_reader = csv.reader(sensor_file)
            for sensor_row in sensor_csv_reader:
                random_equip = random.choice(Equip.objects.all())
                Sensor.objects.create(
                    name=sensor_row[1],
                    series=sensor_row[2],
                    format=sensor_row[3],
                    protocol=sensor_row[4],
                    equip=random_equip,
                )
