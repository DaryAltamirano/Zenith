from django.db import models
import uuid

class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=20, help_text="Enter field documentation")

class Sensor(models.Model):
    class Protocol(models.TextChoices):
        HTTP = 'HTTP'
        MQTT = 'MQTT'

    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=20, help_text="Enter field documentation")
    series = models.IntegerField(help_text="Enter field documentation")
    uuid = models.UUIDField(default=uuid.uuid4, help_text="Enter field documentation", unique=True)
    protocol =   models.CharField(max_length=20, help_text="Enter field documentation",
                                  choices=Protocol.choices, default=Protocol.HTTP)
    zone_id = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)
    created_at = models.DateField('Fecha de creacion', auto_now=True, auto_created=True)

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    headers =  models.CharField(max_length=20, help_text="Enter field documentation")
    format =   models.CharField(max_length=20, help_text="Enter field documentation")
    sensor_id = models.OneToOneField(Sensor, on_delete=models.CASCADE)

class Scheduler(models.Model):
    id = models.AutoField(primary_key=True)
    uri =  models.CharField(max_length=20, help_text="Enter field documentation")
    frequency =   models.CharField(max_length=20, help_text="Enter field documentation")
    timeline =   models.CharField(max_length=20, help_text="Enter field documentation")
    sensor_id = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    created_at = models.DateField('Fecha de creacion', auto_now=True, auto_created=True)
