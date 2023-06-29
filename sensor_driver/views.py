from django.shortcuts import render
from django.http import JsonResponse
from sensor_driver.models import Sensor, Zone
from django.shortcuts import redirect

def listSensor(request):
    from django.forms import models
    sensors = Sensor.objects.all()
    return render(request, 'listSensor/list.html', {"sensors": sensors})

def formSensor(request):
    protocols = ["HTTP", "MQTT"]
    times = ["Second", "Minutes", "Hours"]
    zones = Zone.objects.all()
    return render(request, 'formSensor/form.html', {'protocols': protocols, 'zones': zones, "times": times})

def postZone(request):
    if request.method == 'POST':
        return redirect("/sensor/form/")

    return JsonResponse({"method": "get"})

def postSensor(request):
    if request.method == 'POST':
        return redirect("/sensor/list/")

    return JsonResponse({"method": "get"})
