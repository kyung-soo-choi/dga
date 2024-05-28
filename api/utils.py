import datetime
import requests
from django.utils import timezone
import pytz
from .serializers import WeatherDataSerializer


def process_weather_data(data):
    """
    Wetterdaten verarbeiten und nach Tagen klassifizieren.
    Die Funktion erhält eine Liste von Wetterdaten und erstellt ein Wörterbuch,
    das die maximalen und minimalen Temperaturen, den Wochentag und das Icon für jeden Tag speichert.

    :param data: Das Wetterdaten-JSON von der API.
    :return: Ein Wörterbuch mit den verarbeiteten Wetterdaten.
    """
    results = {}
    for entry in data['list']:
        date = entry['dt_txt'].split(' ')[0]
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        weekday = date_obj.weekday()
        weekday_str = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'][weekday]
        icon = entry['weather'][0]['icon']

        if date not in results:
            results[date] = {
                'max_temp': entry['main']['temp_max'],
                'min_temp': entry['main']['temp_min'],
                'weekday': weekday_str,
                'icon': icon,
            }
        else:
            if entry['main']['temp_max'] > results[date]['max_temp']:
                results[date]['max_temp'] = entry['main']['temp_max']
            if entry['main']['temp_min'] < results[date]['min_temp']:
                results[date]['min_temp'] = entry['main']['temp_min']
            results[date]['weekday'] = weekday_str
            results[date]['icon'] = icon

    return results


def fetch_and_process_weather_data():
    """
    Wetterdaten von der OpenWeatherMap API abrufen und verarbeiten.
    Die Funktion sendet eine Anfrage an die API, verarbeitet die erhaltenen Daten
    und speichert die Ergebnisse in der Datenbank.
    """
    cet = pytz.timezone('Europe/Berlin')
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat': '53.5511',
        'lon': '9.9937',
        'appid': 'ea1c1b8160272a3596d5bf64ebfc5d55'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        processed_weather_data = process_weather_data(weather_data)
        for date_str, data in processed_weather_data.items():
            serializer = WeatherDataSerializer(data={
                'date': date_str,
                'max_temp': data['max_temp'],
                'min_temp': data['min_temp'],
                'weekday': data['weekday'],
                'timestamp': timezone.now().astimezone(cet),
                'icon': data['icon']
            })

            if serializer.is_valid():
                serializer.save()
                print(f"Successfully saved - {timezone.now().astimezone(cet)}")
            else:
                print(serializer.errors)
    else:
        print('error')
