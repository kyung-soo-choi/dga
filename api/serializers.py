from rest_framework import serializers
from .models import WeatherData, TodoData, ScheduleData


class WeatherDataSerializer(serializers.ModelSerializer):
    """
    Serializer-Klasse für WeatherData.
    Diese Klasse serialisiert alle Felder des WeatherData-Modells.
    """
    class Meta:
        model = WeatherData
        fields = '__all__'


class TodoSerializer(serializers.ModelSerializer):
    """
    Serializer-Klasse für TodoData.
    Diese Klasse serialisiert alle Felder des TodoData-Modells.
    """
    class Meta:
        model = TodoData
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer-Klasse für ScheduleData.
    Diese Klasse serialisiert alle Felder des ScheduleData-Modells.
    """
    class Meta:
        model = ScheduleData
        fields = '__all__'
