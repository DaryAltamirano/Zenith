# Use include() to add paths from the catalog application
from django.urls import path
from sensor_driver.views import listSensor, formSensor

urlpatterns = [
    path('list/', listSensor, name="listSensor"),
    path('form/', formSensor, name="formSensor"),
]