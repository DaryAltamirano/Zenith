from django.db import models
import uuid

class Zone(models.Model):
    name =  models.CharField(max_length=20, help_text="Enter field documentation")

class Sensor(models.Model):
    name =  models.CharField(max_length=20, help_text="Enter field documentation")
    series =   models.CharField(max_length=20, help_text="Enter field documentation")
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Enter field documentation")
    protocol =   models.CharField(max_length=20, help_text="Enter field documentation")
    zone_id = models.ForeignKey(Zone, on_delete=models.DO_NOTHING)


class Request(models.Model):
    headers =  models.CharField(max_length=20, help_text="Enter field documentation")
    format =   models.CharField(max_length=20, help_text="Enter field documentation")
    sensor_id = models.OneToOneField(Sensor, on_delete=models.CASCADE, primary_key=True)

class Scheduler(models.Model):
    uri =  models.CharField(max_length=20, help_text="Enter field documentation")
    frequency =   models.CharField(max_length=20, help_text="Enter field documentation")
    timeline =   models.CharField(max_length=20, help_text="Enter field documentation")
    sensor_id = models.OneToOneField(Sensor, on_delete=models.CASCADE, primary_key=True)
