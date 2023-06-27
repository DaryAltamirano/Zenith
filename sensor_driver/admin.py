from django.contrib import admin
from sensor_driver.models import Sensor, Request, Scheduler, Zone

admin.site.register(Sensor)
admin.site.register(Request)
admin.site.register(Scheduler)
admin.site.register(Zone)
