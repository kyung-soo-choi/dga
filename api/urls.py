from django.urls import path, include
from rest_framework import routers

from .views import weather_data_list, TodoViewSet, ScheduleViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)
router.register(r'schedules', ScheduleViewSet)

urlpatterns = [
    path('weather/', weather_data_list, name='weather-list'),
    path('', include(router.urls)),
]
