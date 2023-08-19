from rest_framework import serializers
from sensor_driver.models import Equip, Sensor, HaystackTag

class EquipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equip
        fields = '__all__'

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class HaystackTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HaystackTag
        fields = '__all__'
