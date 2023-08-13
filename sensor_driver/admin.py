from tkinter import E
from django.contrib import admin
from sensor_driver.models import HaystackTag, Sensor, Request, Scheduler, Zone, Space, Equip

admin.site.register(HaystackTag)
admin.site.register(Sensor)
admin.site.register(Request)
admin.site.register(Scheduler)
admin.site.register(Zone)
admin.site.register(Space)
admin.site.register(Equip)