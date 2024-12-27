from django.urls import path
from . import views

urlpatterns = [
    path("get_current_weather/", views.get_current_weather, name="get_current_weather"),
    path("get_day_weather/", views.get_day_weather, name="get_day_weather"),
]