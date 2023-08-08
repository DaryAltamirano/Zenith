# Use include() to add paths from the catalog application
from django.urls import path
from django.contrib.auth import views as auth_views
from sensor_driver.views import updateFormSensor, login_required,listSensor, formSensor, postSensor, postZone, deleteSensor, updateSensor
urlpatterns = [
    path('list/',  login_required(listSensor), name="listSensor"),
    path('form/', formSensor, name="formSensor"),
    path('postSensor/', postSensor, name="postSensor"),
    path('deleteSensor/<int:id>', deleteSensor, name="deleteSensor"),
    path('postZone/', postZone, name="postZone"),
    path('updateSensor/<int:id>', updateSensor, name="updateSensor"),
    path('updateFormSensor/<int:id>', updateFormSensor, name="updateFormSensor"),
]
