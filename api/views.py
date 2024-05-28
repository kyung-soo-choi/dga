from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import WeatherData, TodoData, ScheduleData
from .serializers import WeatherDataSerializer, TodoSerializer, ScheduleSerializer


@api_view(['GET'])
def weather_data_list(request):
    weather_data = WeatherData.objects.all().order_by('-timestamp')[:6]
    serializer = WeatherDataSerializer(weather_data, many=True)
    response = Response(serializer.data)
    return response


class TodoViewSet(viewsets.ModelViewSet):
    queryset = TodoData.objects.all()
    serializer_class = TodoSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = ScheduleData.objects.all()
    serializer_class = ScheduleSerializer
