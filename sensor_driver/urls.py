# Use include() to add paths from the catalog application
from django.urls import path
from sensor_driver.views import listSensor, formSensor, postSensor, postZone

urlpatterns = [
    path('list/', listSensor, name="listSensor"),
    path('form/', formSensor, name="formSensor"),
    path('postSensor/', postSensor, name="postSensor"),
    path('postZone/', postZone, name="postZone"),
]
