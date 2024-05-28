from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
from rest_framework import status
from rest_framework.routers import DefaultRouter
from api.models import WeatherData, TodoData, ScheduleData
from rest_framework.test import APIClient
from api.views import weather_data_list, TodoViewSet, ScheduleViewSet

# Unittests ------------------------------------------------------------------------------------------------------------
class WeatherDataModelTest(TestCase):
    """
    Testklasse für das WeatherData-Modell.
    Testet die Erstellung und String-Darstellung von WeatherData-Instanzen.
    """
    def setUp(self):
        self.weather_data = WeatherData.objects.create(
            timestamp=timezone.now(),
            date=timezone.now().date(),
            max_temp=35.12,
            min_temp=22.34,
            weekday="Monday",
            icon="sunny"
        )

    def test_weather_data_creation(self):
        self.assertIsInstance(self.weather_data, WeatherData)
        self.assertEqual(self.weather_data.weekday, "Monday")
        self.assertEqual(self.weather_data.max_temp, 35.12)
        self.assertEqual(self.weather_data.min_temp, 22.34)
        self.assertEqual(self.weather_data.icon, "sunny")

    def test_weather_data_str_method(self):
        expected_str = (f"Monday ({self.weather_data.date}): Max Temp = 35.12, Min Temp = 22.34, "
                        f"Timestamp = {self.weather_data.timestamp}")
        self.assertEqual(str(self.weather_data), expected_str)


class TodoDataModelTest(TestCase):
    """
    Testklasse für das TodoData-Modell.
    Testet die Erstellung und String-Darstellung von TodoData-Instanzen.
    """
    def setUp(self):
        self.todo_data = TodoData.objects.create(
            title="Test Todo",
            description="This is a test todo.",
            completed=False,
            date=timezone.now().date()
        )

    def test_todo_data_creation(self):
        self.assertIsInstance(self.todo_data, TodoData)
        self.assertEqual(self.todo_data.title, "Test Todo")
        self.assertEqual(self.todo_data.description, "This is a test todo.")
        self.assertFalse(self.todo_data.completed)
        self.assertEqual(self.todo_data.date, timezone.now().date())

    def test_todo_data_str_method(self):
        self.assertEqual(str(self.todo_data), "Test Todo This is a test todo.")


class ScheduleDataModelTest(TestCase):
    """
    Testklasse für das ScheduleData-Modell.
    Testet die Erstellung und String-Darstellung von ScheduleData-Instanzen.
    """
    def setUp(self):
        self.schedule_data = ScheduleData.objects.create(
            title="Test Schedule",
            description="This is a test schedule.",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1)
        )

    def test_schedule_data_creation(self):
        self.assertIsInstance(self.schedule_data, ScheduleData)
        self.assertEqual(self.schedule_data.title, "Test Schedule")
        self.assertEqual(self.schedule_data.description, "This is a test schedule.")
        self.assertEqual(self.schedule_data.start_date, timezone.now().date())
        self.assertEqual(self.schedule_data.end_date, timezone.now().date() + timezone.timedelta(days=1))

    def test_schedule_data_str_method(self):
        self.assertEqual(str(self.schedule_data), "Test Schedule")


# url test
class UrlsTestCase(TestCase):
    """
    Testklasse für URLs.
    Testet die Auflösung der URLs für Wetterdaten, Todos und Zeitpläne.
    """
    def test_weather_data_list_url_is_resolved(self):
        url = reverse('weather-list')
        self.assertEqual(resolve(url).func, weather_data_list)

    def test_todo_list_url_is_resolved(self):
        router = DefaultRouter()
        router.register(r'todos', TodoViewSet)

        url = reverse('tododata-list')
        self.assertEqual(resolve(url).func.cls, TodoViewSet)

    def test_schedule_list_url_is_resolved(self):
        router = DefaultRouter()
        router.register(r'schedules', ScheduleViewSet)

        url = reverse('scheduledata-list')
        self.assertEqual(resolve(url).func.cls, ScheduleViewSet)


class ViewsTests(TestCase):
    """
    Testklasse für Views.
    Testet die API-Endpoints für Wetterdaten, Todos und Zeitpläne.
    """
    def setUp(self):
        self.client = APIClient()

        WeatherData.objects.create(
            timestamp=timezone.now(),
            date=timezone.now().date(),
            max_temp=35.12,
            min_temp=22.34,
            weekday="Monday",
            icon="sunny"
        )

        TodoData.objects.create(
            title="Test Todo",
            description="This is a test todo.",
            completed=False,
            date=timezone.now().date()
        )

        ScheduleData.objects.create(
            title="Test Schedule",
            description="This is a test schedule.",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1)
        )

    def test_weather_data_list(self):
        url = reverse('weather-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_todo_list(self):
        url = reverse('tododata-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_schedule_list(self):
        url = reverse('scheduledata-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


# Integration tests ----------------------------------------------------------------------------------------------------
class IntegrationTests(TestCase):
    """
    Integrationstests für die API-Endpoints.
    Testet die Erstellung und das Abrufen von Daten über die API.
    """
    def setUp(self):
        self.client = APIClient()
        self.weather_url = reverse('weather-list')
        self.todo_url = reverse('tododata-list')
        self.schedule_url = reverse('scheduledata-list')

    def test_create_and_get_weather_data(self):
        """
        Test zur Erstellung und Abruf von Wetterdaten über die API.
        """
        weather_data = {
            'timestamp': timezone.now().isoformat(),
            'date': timezone.now().date().isoformat(),
            'max_temp': 30.5,
            'min_temp': 20.0,
            'weekday': 'Monday',
            'icon': 'sunny'
        }
        response = self.client.post(self.weather_url, weather_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)  # weather_data_list is GET-only
        response = self.client.get(self.weather_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No data should be created with POST

    def test_create_and_get_todo_data(self):
        """
        Test zur Erstellung und Abruf von Todo-Daten über die API.
        """
        todo_data = {
            'title': 'New Todo',
            'description': 'Test Todo description',
            'completed': False,
            'date': timezone.now().date().isoformat()
        }
        response = self.client.post(self.todo_url, todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'New Todo')

    def test_create_and_get_schedule_data(self):
        """
        Test zur Erstellung und Abruf von Zeitplandaten über die API.
        """
        schedule_data = {
            'title': 'New Schedule',
            'description': 'Test Schedule description',
            'start_date': timezone.now().date().isoformat(),
            'end_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
        }
        response = self.client.post(self.schedule_url, schedule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.schedule_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'New Schedule')

    def test_full_integration(self):
        """
        Test zur Integration von Wetter-, Todo- und Zeitplandaten über die API.
        Überprüft die Erstellung und das Abrufen aller Daten.
        """
        # Wetterdaten erstellen (POST nicht erlaubt)
        weather_data = {
            'timestamp': timezone.now().isoformat(),
            'date': timezone.now().date().isoformat(),
            'max_temp': 30.5,
            'min_temp': 20.0,
            'weekday': 'Monday',
            'icon': 'sunny'
        }
        response = self.client.post(self.weather_url, weather_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)  # weather_data_list is GET-only

        # Todo-Daten erstellen
        todo_data = {
            'title': 'New Todo',
            'description': 'Test Todo description',
            'completed': False,
            'date': timezone.now().date().isoformat()
        }
        self.client.post(self.todo_url, todo_data, format='json')

        # Zeitplandaten erstellen
        schedule_data = {
            'title': 'New Schedule',
            'description': 'Test Schedule description',
            'start_date': timezone.now().date().isoformat(),
            'end_date': (timezone.now().date() + timezone.timedelta(days=1)).isoformat()
        }
        self.client.post(self.schedule_url, schedule_data, format='json')

        # Überprüfen, ob die Wetterdaten korrekt abgerufen werden können (GET)
        response = self.client.get(self.weather_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No data should be created with POST

        # Überprüfen, ob die Todo-Daten korrekt abgerufen werden können
        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'New Todo')

        # Überprüfen, ob die Zeitplandaten korrekt abgerufen werden können
        response = self.client.get(self.schedule_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'New Schedule')
