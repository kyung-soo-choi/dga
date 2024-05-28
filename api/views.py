from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import WeatherData, TodoData, ScheduleData
from .serializers import WeatherDataSerializer, TodoSerializer, ScheduleSerializer


@api_view(['GET'])
def weather_data_list(request):
    """
    API-Ansicht zum Abrufen der neuesten 6 Wetterdaten.
    Diese Ansicht gibt die letzten 6 Wetterdaten-Einträge in absteigender Reihenfolge des Zeitstempels zurück.

    :param request: Die HTTP-Anfrage.
    :return: Eine Response mit den serialisierten Wetterdaten.
    """
    weather_data = WeatherData.objects.all().order_by('-timestamp')[:6]
    serializer = WeatherDataSerializer(weather_data, many=True)
    response = Response(serializer.data)
    return response


class TodoViewSet(viewsets.ModelViewSet):
    """
    ViewSet für das TodoData-Modell.
    Dieses ViewSet bietet die Standardaktionen (Listen, Erstellen, Abrufen, Aktualisieren, Löschen) für TodoData.
    """
    queryset = TodoData.objects.all()
    serializer_class = TodoSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet für das ScheduleData-Modell.
    Dieses ViewSet bietet die Standardaktionen (Listen, Erstellen, Abrufen, Aktualisieren, Löschen) für ScheduleData.
    """
    queryset = ScheduleData.objects.all()
    serializer_class = ScheduleSerializer
