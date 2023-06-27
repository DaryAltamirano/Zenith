from django.shortcuts import render, get_object_or_404

from sensor_driver.models import Sensor, Zone


def listSensor(request):
    from django.forms import models
    sensors = Sensor.objects.all()
    return render(request, 'listSensor/list.html', {"sensors": sensors })

def formSensor(request):
    protocols = ["HTTP", "MQTT"]
    zones = Zone.objects.all()
    return render(request, 'formSensor/form.html', {'protocols':protocols, 'zones': zones})