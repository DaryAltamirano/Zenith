# Use include() to add paths from the catalog application
from django.urls import path
from django.contrib.auth import views as auth_views
from sensor_driver.views import deleteEquip, equiplistSensor, updateEquip,updateFormEquip,equipformSensor,postEquip,updateFormSpace, updateSpace,postSpace,spacelistSensor,spaceformSensor,updateFormZone, updateZone,zonelistSensor,zoneformSensor,updateFormSensor, login_required,listSensor, formSensor, postSensor, postZone, deleteSensor, updateSensor

urlpatterns = [
    path('zoneform/',  zoneformSensor, name="zoneformSensor"),
    path('updateFormZone/<int:id>', updateFormZone, name="updateFormZone"),
    path('updateZone/<int:id>', updateZone, name="updateZone"),
    path('zonelist/',  zonelistSensor, name="zonelistSensor"),
    path('postZone/', postZone, name="postZone"),
    
    path('postSpace/', postSpace, name="postSpace"),
    path('spaceform/',  spaceformSensor, name="spaceformSensor"),
    path('updateFormSpace/<int:id>', updateFormSpace, name="updateFormSpace"),
    path('updateSpace/<int:id>', updateSpace, name="updateSpace"),
    path('spacelist/',  spacelistSensor, name="spacelistSensor"),
    
    path('postEquip/', postEquip, name="postEquip"),
    path('equipform/',  equipformSensor, name="equipformSensor"),
    path('updateFormEquip/<int:id>', updateFormEquip, name="updateFormEquip"),
    path('updateEquip/<int:id>', updateEquip, name="updateEquip"),
    path('equiplist/',  equiplistSensor, name="equiplistSensor"),
    path('deleteEquip/<int:id>', deleteEquip, name="deleteEquip"),

    path('list/',  login_required(listSensor), name="listSensor"),
    path('form/', formSensor, name="formSensor"),
    path('postSensor/', postSensor, name="postSensor"),
    path('deleteSensor/<int:id>', deleteSensor, name="deleteSensor"),
    path('updateSensor/<int:id>', updateSensor, name="updateSensor"),
    path('updateFormSensor/<int:id>', updateFormSensor, name="updateFormSensor"),
]
