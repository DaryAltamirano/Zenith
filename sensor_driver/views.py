import json
from django.shortcuts import render
from django.http import JsonResponse
from sensor_driver.management.commands.supports.ConnectionRabbitMQ import ConnectionRabbitMQ
from sensor_driver.models import Sensor, Zone, Request as Request_Model, Scheduler
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view


def listSensor(request):
    sensors = Sensor.objects.all()
    return render(request, 'listSensor/list.html', {"sensors": sensors})

def formSensor(request):
    protocols = ["HTTP", "MQTT"]
    measures = ["SECONDS", "MINUTES", "HOURS"]
    zones = Zone.objects.all()
    return render(request, 'formSensor/form.html', {'protocols': protocols, 'zones': zones, "measures": measures})

def updateFormSensor(request, id):
    sensor = Sensor.objects.filter(id=id).get()

    zone = sensor.zone
    data = {
        "sensor": sensor,
        "zone": zone
    }

    if (sensor.protocol == "HTTP"):
        scheduler = Scheduler.objects.filter(sensor_id = sensor.id).get()
        request_data = Request_Model.objects.filter(sensor_id = sensor.id).get()

        data.update({
            "scheduler" : scheduler,
            "request_data" : request_data
        })

    return render(request,'formSensor/updateSensor.html', data)

@api_view(['POST'])
def updateSensor(request, id):
    data = request.data

    sensor = Sensor.objects.filter(id=id).get()
    
    sensor.name= data.get('name')
    sensor.series= data.get('serial')
    sensor.format = data.get('body_request')
    sensor.save()

    scheduler = Scheduler.objects.filter(sensor_id = sensor.id).get()
    request_data = Request_Model.objects.filter(sensor_id = sensor.id).get()  
    
    request_data.headers= data.get('body_headers')
    request_data.params = data.get('body_params')
    request_data.save()
    
    scheduler.uri= data.get('uri')
    scheduler.measure= data.get('measure')
    scheduler.timeline= data.get('number')
    scheduler.save()
    
    rabbitMq = ConnectionRabbitMQ()
    channel = rabbitMq.channel()

    rabbitMq.basicPublish(channel, json.dumps({"sensor_id": sensor.id }), "update_sensor")
    return redirect("/sensor/list/")

@api_view(['POST'])
def postZone(request):
    data = request.data
    zone = Zone(name=data.get("name"))
    zone.save()
    return redirect("/sensor/form/")



@api_view(['POST'])
def postSensor(request):
    data = request.data

    zone = Zone.objects.get(id = data.get('zone'))
    
    sensor = Sensor(
        name= data.get('name'),
        series= data.get('serial'),
        protocol= data.get('protocol'),
        format = data.get('body_request'),
        zone= zone
        )
    sensor.save()

    if (data.get('protocol') == "HTTP"): 
        request_data = Request_Model(
            headers= data.get('body_headers'),
            params = data.get('body_params'),
            sensor = sensor
            )
        request_data.save()
        scheduler_data = Scheduler(
            uri= data.get('uri'),
            measure= data.get('measure'),
            timeline= data.get('number'),
            sensor = sensor
            )
        scheduler_data.save()
    rabbitMq = ConnectionRabbitMQ()
    channel = rabbitMq.channel()

    rabbitMq.basicPublish(channel, json.dumps({"sensor_id": sensor.id }), "new_sensor")
    return redirect("/sensor/list/")
 
@api_view(['DELETE'])
def deleteSensor(request, id):
    Sensor.objects.filter(id=id).delete()
    return JsonResponse({"status":"ok"})

