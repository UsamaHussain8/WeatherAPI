from .models import CurrentForecast
from rest_framework import serializers

class CurrentForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentForecast
        fields = '__all__'