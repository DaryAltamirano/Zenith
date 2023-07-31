from django.db import models
import uuid
from django.db.models import JSONField

class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

class HaystackTag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

class Sensor(models.Model):
    class Protocol(models.TextChoices):
        HTTP = 'HTTP'
        MQTT = 'MQTT'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    series = models.CharField(max_length=100, null=False)
    format = JSONField()
    protocol = models.CharField(max_length=20,choices=Protocol.choices, default=Protocol.HTTP)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)
    created_at = models.DateField('Fecha de creacion', auto_now=True, auto_created=True)

class Scheduler(models.Model):
    class Measure(models.TextChoices):
        SECONDS = 'SECONDS'
        MINUTES = 'MINUTES'
        HOURS = 'HOURS'

    id = models.AutoField(primary_key=True)
    uri = models.CharField(max_length=100)
    measure = models.CharField(max_length=20,choices=Measure.choices, default=Measure.MINUTES)
    timeline = models.CharField(max_length=20)
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    created_at = models.DateField('Fecha de creacion', auto_now=True, auto_created=True)
    active = models.BooleanField(default=True)

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    headers = JSONField(null= True)
    params = JSONField(null= True)
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
