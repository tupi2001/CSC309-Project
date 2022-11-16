from rest_framework import serializers

from classes.models import Class
from studios.serializers import StudioSerializer


class ClassSerializer(serializers.ModelSerializer):
    studio = StudioSerializer()

    class Meta:
        model = Class
        fields = ['id', 'studio', 'name', 'description', 'coach', 
            'keywords', 'capacity', 'start_time', 'end_time', 'end_date']