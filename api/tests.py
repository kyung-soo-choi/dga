from django.test import TestCase
from django.urls import reverse, resolve
from django.utils import timezone
from rest_framework import status
from rest_framework.routers import DefaultRouter
from api.models import WeatherData, TodoData, ScheduleData
from rest_framework.test import APIClient
from api.views import weather_data_list, TodoViewSet, ScheduleViewSet


# model test
class WeatherDataModelTest(TestCase):

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
