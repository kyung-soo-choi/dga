from rest_framework import serializers
from .models import WeatherData, TodoData, ScheduleData


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoData
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleData
        fields = '__all__'