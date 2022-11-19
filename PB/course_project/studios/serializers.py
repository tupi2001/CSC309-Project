from rest_framework import serializers
from .models import Studio

class StudioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Studio
        fields = ['id', 'name', 'address', 'latitude',
<<<<<<< HEAD
                  'longitude', 'postal', 'phone_number']
=======
                  'longitude', 'postal', 'phone_number']
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
