from django.shortcuts import render
from django.http import JsonResponse
from sensor_driver.models import Sensor, Zone, Request as Request_Model
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view


def listSensor(request):
    sensors = Sensor.objects.all()
    return render(request, 'listSensor/list.html', {"sensors": sensors})


def formSensor(request):
    protocols = ["HTTP", "MQTT"]
    times = ["Second", "Minutes", "Hours"]
    zones = Zone.objects.all()
    return render(request, 'formSensor/form.html', {'protocols': protocols, 'zones': zones, "times": times})


@api_view(['POST'])
def postZone(request):
    data = request.data
    zone = Zone(name=data.get("name"))
    zone.save()
    return redirect("/sensor/form/")


@api_view(['POST'])
def postSensor(request):
    data = request.data

    request_data = Request_Model(format=data.get('body'))
    request_data.save()

    zone = Zone.objects.get(id = data.get('zone'))

    sensor = Sensor(name=data.get('body'), series=data.get('serial'), protocol=data.get('protocol'),
                    request=request_data, zone= zone)
    sensor.save()
    return redirect("/sensor/list/")
