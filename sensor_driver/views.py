import json
from multiprocessing import connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from sensor_driver.management.commands.supports.ConnectionRabbitMQ import ConnectionRabbitMQ
from sensor_driver.models import HaystackTag, Sensor, Zone,Space, Equip,  Request as Request_Model, Scheduler
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view


@login_required(login_url="/login/")
def formSensor(request):
    protocols = ["HTTP", "MQTT"]
    tags = HaystackTag.objects.all()
    equips = Equip.objects.all()
    measures = ["SECONDS", "MINUTES", "HOURS"]
    zones = Zone.objects.all()
    return render(request, 'formSensor/form.html', {'protocols': protocols, 'zones': zones, 'equips': equips,"measures": measures, "tags": tags})

@login_required(login_url="/login/")
def listSensor(request):
    sensors = Sensor.objects.all()
    return render(request, 'listSensor/list.html', {"sensors": sensors})



@login_required(login_url="/login/")
def zonelistSensor(request):
    zones = Zone.objects.all()
    return render(request, 'listSensor/zonelist.html', {"zones": zones})

@login_required(login_url="/login/")
def zoneformSensor(request):
    tags = HaystackTag.objects.all()
    return render(request, 'formSensor/zoneform.html', {"tags": tags})



@login_required(login_url="/login/")
def spacelistSensor(request):
    spaces = Space.objects.all()
    return render(request, 'listSensor/spacelist.html', {"spaces": spaces})

@login_required(login_url="/login/")
def spaceformSensor(request):
    tags = HaystackTag.objects.all()
    zones = Zone.objects.all()
    return render(request, 'formSensor/spaceform.html', {"tags": tags, "zones": zones})



@login_required(login_url="/login/")
def equiplistSensor(request):
    equips = Equip.objects.all()
    return render(request, 'listSensor/equiplist.html', {"equips": equips})

@login_required(login_url="/login/")
def equipformSensor(request):
    tags = HaystackTag.objects.all()
    spaces = Space.objects.all()
    zones = Zone.objects.all()
    return render(request, 'formSensor/equipform.html', {"tags": tags, "zones": zones, "spaces": spaces})


@login_required(login_url="/login/")
def updateFormZone(request, id):
    zone = Zone.objects.filter(id=id).get()
    tags = HaystackTag.objects.all()
    data = {
        "zone": zone,
        "tags": tags
    }
    return render(request, 'formSensor/updateZone.html', data)

@login_required(login_url="/login/")
def updateFormSensor(request, id):
    sensor = Sensor.objects.filter(id=id).get()
    tags = HaystackTag.objects.all()
    equips = Equip.objects.all()
    data = {
        "sensor": sensor,
        "equips": equips,
        "tags": tags
    }

    scheduler = ""
    if sensor.protocol == "http":
        scheduler = Scheduler.objects.filter(sensor_id=sensor.id).get()

    request_data = Request_Model.objects.filter(sensor_id=sensor.id).get()

    data.update({
        "request_data": request_data,
        "scheduler":scheduler
    })

    return render(request, 'formSensor/updateSensor.html', data)

@login_required(login_url="/login/")
def updateFormSpace(request, id):
    space = Space.objects.filter(id=id).get()
    zone = Zone.objects.all()
    tags = HaystackTag.objects.all()
    data = {
        "zones": zone,
        "space": space,
        "tags": tags
    }
    return render(request, 'formSensor/updateSpace.html', data)

@login_required(login_url="/login/")
def updateFormEquip(request, id):
    equip = Equip.objects.filter(id=id).get()
    spaces = Space.objects.all()
    zone = Zone.objects.all()
    tags = HaystackTag.objects.all()
    data = {
        "equip": equip,
        "zones": zone,
        "spaces": spaces,
        "tags": tags
    }
    return render(request, 'formSensor/updateEquip.html', data)




@login_required(login_url="/login/")
@api_view(['POST'])
def updateSensor(request, id):
    data = request.data

    sensor = Sensor.objects.filter(id=id).get()

    sensor.name = data.get('name')
    sensor.series = data.get('serial')
    sensor.format = data.get('body_request')
    sensor.save()

    scheduler = Scheduler.objects.filter(sensor_id=sensor.id).get()
    request_data = Request_Model.objects.filter(sensor_id=sensor.id).get()

    request_data.headers = data.get('body_headers')
    request_data.params = data.get('body_params')
    request_data.save()

    scheduler.uri = data.get('uri')
    scheduler.measure = data.get('measure')
    scheduler.timeline = data.get('number')
    scheduler.save()

    rabbitMq = ConnectionRabbitMQ()
    channel = rabbitMq.channel()

    rabbitMq.basicPublish(channel, json.dumps({"sensor_id": sensor.id, "action": "update_sensor"}),
                          "scheduler_cron_jobs")
    return redirect("/sensor/list/")

@login_required(login_url="/login/")
@api_view(['POST'])
def updateZone(request, id):
    data = request.data

    zone = Zone.objects.filter(id=id).get()

    zone.name = data.get('name')
    zone.geoAddr = data.get('geoAddr')
    zone.geoCoord = data.get('geoCoord')
    zone.tz = data.get('time_zone')
    zone.save()

    return redirect("/sensor/zonelist/")

@login_required(login_url="/login/")
@api_view(['POST'])
def updateSpace(request, id):
    data = request.data

    space = Space.objects.filter(id=id).get()
    zone = Zone.objects.get(id=data.get('zone'))
    
    space.name = data.get('name')
    space.area = data.get('area')
    space.spaceref = data.get('spaceref')
    space.zone = zone
    space.save()

    return redirect("/sensor/spacelist/")

@login_required(login_url="/login/")
@api_view(['POST'])
def updateEquip(request, id):
    data = request.data

    equip = Equip.objects.filter(id=id).get()
    zone = Zone.objects.get(id=data.get('zone'))
    space = Space.objects.get(id=data.get('space'))

    equip.name = data.get('name')
    equip.equipref = data.get('equipref')
    equip.zone = zone
    equip.space = space
    equip.save()

    return redirect("/sensor/equiplist/")



@login_required(login_url="/login/")
@api_view(['POST'])
def postZone(request):
    data = request.data
    zone = Zone(name=data.get("name"), 
                geoAddr=data.get("geoAddr"),
                geoCoord=data.get("geoCoord"),
                tz=data.get("time_zone"))
    zone.save()
    return redirect("/sensor/zonelist/")

@login_required(login_url="/login/")
@api_view(['POST'])
def postSpace(request):
    data = request.data
    zone = Zone.objects.get(id=data.get('zone'))
    space = Space(name=data.get("name"), 
                  zone=zone,
                  area=data.get("area"),
                  spaceref=data.get("spaceref"))
    space.save()
    return redirect("/sensor/spacelist/")

@login_required(login_url="/login/")
@api_view(['POST'])
def postEquip(request):
    data = request.data
    space = Space.objects.get(id=data.get('space'))
    equip = Equip(name=data.get("name"), 
                  zone=space.zone,
                  space=space,
                  equipref=data.get("equipref"))
    equip.save()
    return redirect("/sensor/equiplist/")

@login_required(login_url="/login/")
@api_view(['POST'])
def postSensor(request):
    data = request.data
    print(data)
    body_list = []
    time_list = []
    for key, value, categoryvalue in zip(data.getlist('baseBodyKey'), data.getlist('baseBodyValue'), data.getlist('baseCategoryValue')):
        body_dict = {
            key: value,
            "category": categoryvalue
        }
        body_list.append(body_dict)
    body_json = json.dumps(body_list)

    equip = Equip.objects.get(id=data.get('equip'))

    sensor = Sensor(
        name=data.get('name'),
        series=data.get('serial'),
        protocol=data.get('protocol'),
        format=body_json,
        equip=equip,
        zone=equip.zone
    )
    sensor.save()

    if data.get('protocol') == "mqtt":
        conecction_dict = {
            "broker": data.get('uri'),
            "user": data.get('user'),
            "password": data.get('password'),
            "port": data.get('port'),
            "topic": data.get('topic')
        }
    if data.get('protocol') == "modbus":
        conecction_dict = {
            "uri": data.get('uri'),
            "address": data.get('address'),
            "communication": data.get('comunicacion'),
            "port": data.get('port')
        }
    if data.get('protocol') == "coap":
        time_list.append(data.get('minute'))
        time_list.append("/" + str(data.get('hora')))
        timescheduler = ' '.join(map(str, time_list))
        
        conecction_dict = {
            "uri": data.get('uri'),
            "method":  data.get('hora'),
            "port": data.get('port')
        }
        scheduler_data = Scheduler(
            timeline=timescheduler,
            sensor=sensor
        )
        scheduler_data.save()

    if data.get('protocol') == "http":
        params_dict = {key: value for key, value in zip(data.get('baseParamKey'), data.get('baseParamValue'))}
        headers_dict = {key: value for key, value in zip(data.get('baseHeaderKey'), data.get('baseHeaderValue'))}
        time_list.append(data.get('minutehttp'))
        time_list.append('/' + str(data.get('horahttp')))
        timescheduler = ' '.join(map(str, time_list))
        conecction_dict = {
            "uri": data.get('uri'),
            "method": data.get('method'),
            "params": params_dict,
            "headers": headers_dict
        }
        scheduler_data = Scheduler(
            timeline=timescheduler,
            sensor=sensor
        )
        scheduler_data.save()

    request_data = Request_Model(
        connection=json.dumps(conecction_dict),
        sensor=sensor
    )
    request_data.save()
    

    rabbitMq = ConnectionRabbitMQ()
    channel = rabbitMq.channel()

    rabbitMq.basicPublish(channel, json.dumps({"sensor_id": sensor.id, "action": "new_sensor"}), "scheduler_cron_jobs")
    return redirect("/sensor/list/")


@login_required
@api_view(['DELETE'])
def deleteSensor(request, id):
    sensor = Sensor.objects.filter(id=id).get()
    Request_Model.objects.filter(sensor=sensor).delete()
    
    if sensor.protocol == "coap":
        Scheduler.objects.filter(sensor=sensor).delete()
    if sensor.protocol == "http":
        Scheduler.objects.filter(sensor=sensor).delete()

    Sensor.objects.filter(id=id).delete()
    rabbitMq = ConnectionRabbitMQ()
    channel = rabbitMq.channel()
    print('respuesta')
    rabbitMq.basicPublish(channel, json.dumps({"sensor_id": id, "action": "delete_sensor"}), "scheduler_cron_jobs")
    return JsonResponse({"status": "ok"})

@login_required
@api_view(['DELETE'])
def deleteEquip(request, id):
    Equip.objects.filter(id=id).delete()
    return JsonResponse({"status": "ok"})



