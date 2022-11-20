from rest_framework import serializers
from .models import Studio

class StudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Studio
        fields = ['id', 'name', 'address', 'latitude',
                  'longitude', 'postal', 'phone_number']
