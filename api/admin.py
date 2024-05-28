from django.contrib import admin
from .models import WeatherData, TodoData, ScheduleData

admin.site.register(WeatherData)
admin.site.register(TodoData)
admin.site.register(ScheduleData)
