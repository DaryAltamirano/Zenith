from django.db import models
import uuid


class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    headers = models.CharField(max_length=2000, null=True)
    format = models.CharField(max_length=2000, null=False)


class Sensor(models.Model):
    class Protocol(models.TextChoices):
        HTTP = 'HTTP'
        MQTT = 'MQTT'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    series = models.CharField(max_length=100, null=False)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    protocol = models.CharField(max_length=20,choices=Protocol.choices, default=Protocol.HTTP)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)
    created_at = models.DateField('Fecha de creacion', auto_now=True, auto_created=True)
    request = models.OneToOneField(Request, on_delete=models.CASCADE)


class Scheduler(models.Model):
    id = models.AutoField(primary_key=True)
    uri = models.CharField(max_length=20)
    measure = models.CharField(max_length=20)
    timeline = models.CharField(max_length=20)
    sensor_id = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    created_at = models.DateField('Fecha de creacion', auto_now=True, auto_created=True)
