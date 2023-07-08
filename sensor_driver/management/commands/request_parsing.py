from django.core.management.base import BaseCommand
import pika
import sys

from sensor_driver.management.commands.supports.ConnectionRabbitMQ import ConnectionRabbitMQ

class Command(BaseCommand):
    help = 'Displays current time'
    #def add_arguments(self, parser):

    def add_arguments(self, parser):
        parser.add_argument('-qn', '--queue_name', type=str, help='Queue Name')


    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)


    def handle(self, *args, **kwargs):
        queue_name = kwargs['queue_name']

        channel = ConnectionRabbitMQ().channel()

        ConnectionRabbitMQ().basicConsume(channel, self.callback, queue_name)
