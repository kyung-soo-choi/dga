from django.urls import path, include
from rest_framework import routers

from .views import weather_data_list, TodoViewSet, ScheduleViewSet

# Router für Todo- und Schedule-ViewSets initialisieren
router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)
router.register(r'schedules', ScheduleViewSet)

# URL-Muster definieren
urlpatterns = [
    # Pfad für die Wetterdatenliste
    path('weather/', weather_data_list, name='weather-list'),
    # Inkludieren der vom Router generierten URLs
    path('', include(router.urls)),
]
