from django.db import models

class CurrentForecast(models.Model):
    date = models.DateTimeField()
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    temperature_feels_like = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    sunrise = models.TimeField(default="06:00:00")
    sunset = models.TimeField(default="18:00:00")
    weather_description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} - {self.date}"

class WeatherForecast(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    days = models.ManyToManyField(CurrentForecast)