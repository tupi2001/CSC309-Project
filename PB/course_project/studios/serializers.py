from rest_framework import serializers
from .models import Studio

class StudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Studio
        fields = ['name', 'address', 'latitude',
                  'longitude', 'postal_code', 'phone_number']

class DistanceSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
