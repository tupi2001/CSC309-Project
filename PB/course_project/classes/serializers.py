from rest_framework import serializers

from classes.models import Class, UserAndClass
from studios.serializers import StudioSerializer
from accounts.serializers import CreateUserSerializer


class ClassSerializer(serializers.ModelSerializer):
    studio = StudioSerializer()

    class Meta:
        model = Class
        fields = ['id', 'studio', 'name', 'description', 'coach', 
            'keywords', 'capacity', 'recurrences', 'start_time', 'end_time']

class UserAndClassSerializer(serializers.ModelSerializer):
    classes = ClassSerializer()
    users = CreateUserSerializer()

    class Meta:
        model = UserAndClass
        fields = ['class', 'users']