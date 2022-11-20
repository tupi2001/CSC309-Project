from rest_framework import serializers
from .models import Studio

class StudioSerializer(serializers.ModelSerializer):
    """Serializer for a studio"""

    class Meta:
        """Holds the model of the Studio and its specific fields that will be displayed on the UI"""
        model = Studio
        fields = ['name', 'address', 'latitude',
                  'longitude', 'postal_code', 'phone_number']

class DistanceSerializer(serializers.Serializer):
    """Holds the longitude and latitude of a studio"""
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
