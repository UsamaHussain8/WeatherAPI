import os
import environ
import requests
import json
from datetime import datetime, timedelta, timezone

from django.shortcuts import render
from django.http import JsonResponse
from .models import CurrentForecast
from .serializers import CurrentForecastSerializer

from .utils import get_city_geopoints, get_city_name, get_datetime

env = environ.Env()
environ.Env.read_env()
API_KEY = env('API_KEY')

def get_current_weather(request):
    city_data = get_city_geopoints("Islamabad")
    city_lat = city_data[0]["lat"]
    city_long = city_data[0]["lon"]

    weather_json_response = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={city_lat}&lon={city_long}&exclude=minutely,hourly&appid={API_KEY}&units=metric")
    weather_data = json.loads(weather_json_response.text)
    #print(weather_data.keys())

    local_time = get_datetime(weather_data, 'dt')
    sunrise_time = get_datetime(weather_data, 'sunrise')
    sunset_time = get_datetime(weather_data, 'sunset')
    city_name = get_city_name(city_lat, city_long)

    current_data = {
        'temperature': weather_data['current']['temp'],
        'temperature_feels_like': weather_data['current']['feels_like'],
        'humidity': weather_data['current']['humidity'],
        'wind_speed': weather_data['current']['wind_speed'],
        'weather_description': weather_data['current']['weather'][0]['description'],
        'date': local_time,
        "city": city_name,
        "sunrise": sunrise_time,
        "sunset": sunset_time
    }

    current_forecast = CurrentForecast.objects.create(**current_data)
    serializer = CurrentForecastSerializer(current_forecast)

    return JsonResponse(serializer.data, safe=False)