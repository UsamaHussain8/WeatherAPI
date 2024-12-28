import os
import environ
import requests
import json
from datetime import datetime, timedelta, timezone

from django.shortcuts import render
from django.http import JsonResponse
from .models import CurrentForecast, WeatherForecast
from .serializers import CurrentForecastSerializer, WeatherForecastSerializer

from .utils import get_city_geopoints, get_city_name, get_datetime

env = environ.Env()
environ.Env.read_env()
API_KEY = env('API_KEY')

def get_current_weather(request):
    city_data = get_city_geopoints(request.GET.get('city', 'Islamabad'))
    city_lat = city_data[0]["lat"]
    city_long = city_data[0]["lon"]

    weather_json_response = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={city_lat}&lon={city_long}&exclude=minutely,hourly&appid={API_KEY}&units=metric")
    weather_data = json.loads(weather_json_response.text)
    current_weather_data = weather_data['current']

    local_time = get_datetime(current_weather_data, 'dt')
    sunrise_time = get_datetime(current_weather_data, 'sunrise')
    sunset_time = get_datetime(current_weather_data, 'sunset')
    city_name = get_city_name(city_lat, city_long)

    current_data = {
        'temperature': current_weather_data['temp'],
        'temperature_feels_like': current_weather_data['feels_like'],
        'humidity': current_weather_data['humidity'],
        'wind_speed': current_weather_data['wind_speed'],
        'weather_description': current_weather_data['weather'][0]['description'],
        'date': local_time,
        "city": city_name,
        "sunrise": sunrise_time,
        "sunset": sunset_time
    }

    current_forecast = CurrentForecast.objects.create(**current_data)
    serializer = CurrentForecastSerializer(current_forecast)

    return JsonResponse(serializer.data, safe=False)

def get_day_weather(request):
    city_data = get_city_geopoints(request.GET.get('city', 'Islamabad'))
    city_lat = city_data[0]["lat"]
    city_long = city_data[0]["lon"]

    weather_json_response = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={city_lat}&lon={city_long}&exclude=minutely,hourly&appid={API_KEY}&units=metric")
    weather_data = json.loads(weather_json_response.text)
    daily_weather_data = weather_data['daily']
    weather_forecast = WeatherForecast.objects.create()

    for day in daily_weather_data:
        local_time = get_datetime(day, 'dt')
        sunrise_time = get_datetime(day, 'sunrise')
        sunset_time = get_datetime(day, 'sunset')
        city_name = get_city_name(city_lat, city_long)
        
        # Prepare data for CurrentForecast
        current_data = {
            'temperature': day['temp']['day'],
            'temperature_feels_like': day['feels_like']['day'],
            'humidity': day['humidity'],
            'wind_speed': day['wind_speed'],
            'weather_description': day['weather'][0]['description'],
            'date': local_time,
            'city': city_name,
            'sunrise': sunrise_time,
            'sunset': sunset_time,
        }

        # Create CurrentForecast and link to WeatherForecast
        current_forecast = CurrentForecast.objects.create(**current_data)
        weather_forecast.days.add(current_forecast)

    # Serialize the WeatherForecast instance
    serializer = WeatherForecastSerializer(weather_forecast)

    return JsonResponse(serializer.data, safe=False)