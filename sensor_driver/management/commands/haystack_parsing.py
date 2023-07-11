from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from django.utils import timezone
from sensor_driver.management.commands.supports.ConnectionRabbitMQ import ConnectionRabbitMQ
import sys
import pika
import requests

class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('-qn', '--queue_name', type=str, help='Queue Name')


    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)


    def handle(self, *args, **kwargs):
        queue_name = kwargs['queue_name']

        channel = ConnectionRabbitMQ().channel()

        ConnectionRabbitMQ().basicConsume(channel, self.callback, queue_name)
