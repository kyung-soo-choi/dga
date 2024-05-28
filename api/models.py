from django.db import models


class WeatherData(models.Model):
    timestamp = models.DateTimeField()
    date = models.DateField()
    max_temp = models.DecimalField(max_digits=5, decimal_places=2)
    min_temp = models.DecimalField(max_digits=5, decimal_places=2)
    weekday = models.CharField(max_length=20)
    icon = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.weekday} ({self.date}): Max Temp = {self.max_temp}, Min Temp = {self.min_temp}, Timestamp = {self.timestamp}"


class TodoData(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    date = models.DateField()  # Add this line

    def __str__(self):
        return self.title


class ScheduleData(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title