from django.db import models
import uuid
import csv
from django.db.models import JSONField
from django.core.exceptions import ValidationError
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Zone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    geoAddr = models.CharField(max_length=255)
    geoCoord = models.CharField(max_length=255)
    tz = models.CharField(max_length=30)    

class Space(models.Model):
    id = models.AutoField(primary_key=True)
    spaceref = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)

class Equip(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    equipref = models.CharField(max_length=50)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)
    space = models.ForeignKey(Space, on_delete=models.DO_NOTHING)

class HaystackTag(models.Model):
    id = models.CharField(primary_key=True, max_length=50 ,unique=True) 
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    state = models.CharField(max_length=1)

class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    series = models.CharField(max_length=100, null=False)
    format = JSONField()
    protocol = models.CharField(max_length=50)
    equip = models.ForeignKey(Equip, on_delete=models.DO_NOTHING)
    zone = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)
    created_at = models.DateField('Fecha de creacion', auto_now=True, auto_created=True)

class Scheduler(models.Model):
    id = models.AutoField(primary_key=True)
    timeline = models.CharField(max_length=50)
    sensor = models.OneToOneField(Sensor, on_delete=models.DO_NOTHING)
    created_at = models.DateField('Fecha de creacion', auto_now=True, auto_created=True)
    active = models.BooleanField(default=True)

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    connection = JSONField(null= True)
    sensor = models.OneToOneField(Sensor, on_delete=models.DO_NOTHING)
