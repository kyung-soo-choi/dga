import datetime
import requests
from django.utils import timezone
import pytz
from rest_framework.response import Response

from .serializers import WeatherDataSerializer


def process_weather_data(data):
    # Initialisierung des Wörterbuchs zur Speicherung der Ergebnisse
    results = {}

    # Durchlauf der Datenliste
    for entry in data['list']:
        # Datum extrahieren, um Daten nach Tagen zu klassifizieren
        date = entry['dt_txt'].split(' ')[0]  # 'YYYY-MM-DD'
        # Datumstring in ein datetime-Objekt umwandeln, um den Wochentag zu erhalten
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        # Wochentag als Integer (0: Montag, 1: Dienstag, ..., 6: Sonntag)
        weekday = date_obj.weekday()
        # Wochentag in einen lesbaren String umwandeln
        weekday_str = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'][weekday]
        icon = entry['weather'][0]['icon']  # 날씨 아이콘 추출

        # Falls für das Datum kein Eintrag vorhanden ist, mit einem neuen Schlüssel initialisieren
        if date not in results:
            results[date] = {
                'max_temp': entry['main']['temp_max'],
                'min_temp': entry['main']['temp_min'],
                'weekday': weekday_str,
                'icon': icon,
            }
        else:
            # Aktualisierung der Höchst- und Tiefstwerte für bereits vorhandene Daten
            if entry['main']['temp_max'] > results[date]['max_temp']:
                results[date]['max_temp'] = entry['main']['temp_max']
            if entry['main']['temp_min'] < results[date]['min_temp']:
                results[date]['min_temp'] = entry['main']['temp_min']
            results[date]['weekday'] = weekday_str
            results[date]['icon'] = icon  # 아이콘 업데이트

    return results


def fetch_and_process_weather_data():
    cet = pytz.timezone('Europe/Berlin')
    # Einstellung des API-Endpoints und der Parameter
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat': '53.5511',  # Breitengrad
        'lon': '9.9937',  # Längengrad
        'appid': 'ea1c1b8160272a3596d5bf64ebfc5d55'  # API-Schlüssel
    }

    # GET-Anfrage an externe API senden
    response = requests.get(url, params=params)

    # Antwort überprüfen
    if response.status_code == 200:
        weather_data = response.json()  # JSON-Antwort in Python-Objekt umwandeln
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
