from .models import CurrentForecast
from rest_framework import serializers

class CurrentForecastSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%B-%Y (%A) %I:%M:%S %p")
    sunrise = serializers.TimeField(format="%I:%M:%S %p")
    sunset = serializers.TimeField(format="%I:%M:%S %p")

    class Meta:
        model = CurrentForecast
        fields = '__all__'