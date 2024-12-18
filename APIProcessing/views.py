import requests
import json
from django.shortcuts import render
from django.http import JsonResponse

import os
import environ
env = environ.Env()
environ.Env.read_env()
API_KEY = env('API_KEY')

def get_weather(request):
    city = "Islamabad"
    geo_json_response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}")
    city_data = json.loads(geo_json_response.text)
    city_lat = city_data[0]["lat"]
    city_lon = city_data[0]["lon"]

    weather_json_response = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={city_lat}&lon={city_lon}&exclude=minutely,hour")

    return JsonResponse({"city": weather_json_response.json()})

