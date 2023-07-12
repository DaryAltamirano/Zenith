from django.core.management.base import BaseCommand
from sensor_driver.management.commands.supports.ConnectionRabbitMQ import ConnectionRabbitMQ
import sys
import pika
import requests
import json
from sensor_driver.management.commands.supports.ApiConsume import ApiConsume

class Command(BaseCommand):
    help = 'Displays current time'

    Api = ApiConsume()

    rabbitMq = ConnectionRabbitMQ()


    def add_arguments(self, parser):
        parser.add_argument('-uuid', '--uuid_sensor', type=str, help='Uuid Sensor')
        parser.add_argument('-qn', '--queue_name', type=str, help='Queue Name')


    def handle(self, *args, **kwargs):
        uuid = kwargs['uuid_sensor']
        queue = kwargs['queue_name']
        #//uuid obtener toda la infor del dispositivo 

        API_KEY = "eChX8mCYibGmYb0qlcZX3cmxOQf7xgO2qcWCEplw49ixpy6V"
        params = {}
        params['key'] = API_KEY

        url = "https://api.kaiterra.com/v1/lasereggs/dd85475c-a5ef-4a15-b00f-206e408528b2"

        body = self.Api.request(url, params, {})
        channel = self.rabbitMq.channel()
        print(json.dumps(body))
        self.rabbitMq.basicPublish(channel, json.dumps(body), queue)