from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Studio
import json
import math


# Create your views here.

@api_view(['POST'])
def AllStudios(request):
    if request.method == 'POST':
        payload = json.loads(request.body)

        user_latitude = payload.get('latitude', '')
        user_longitude = payload.get('longitude', '')

        if user_latitude == '' or user_longitude == '':
            raise ValidationError

        studio_query = Studio.objects.all()
        response = {}
        studios = []

        for element in studio_query:
            studio = element.__dict__
            studio.pop('_state')

            url_destination = studio['address'].replace(' ', '+') + '+' + studio['postal'].replace(
                '', '+')

            url = "http://maps.google.com/maps/dir/" + str(user_latitude) + ",+" + str(
                user_longitude) + "/" + url_destination

            latitude_difference = abs(studio['latitude'] - user_latitude) * 111.1
            longitude_difference = abs(studio['longitude'] - user_longitude) * 111.1

            distance = math.sqrt(latitude_difference ** 2 + longitude_difference ** 2)
            studio['distance'] = round(distance, 2)

            studio.pop('latitude')
            studio.pop('longitude')
            studio.pop('phone_number')
            studio.pop('postal')
            studio['directions'] = url

            studios.append(studio)

        studios = sorted(studios, key=lambda d: d['distance'])

        for element in studios:
            response[element['name']] = studios

        return JsonResponse(response)


@api_view(['GET'])
def StudioInformation(request, id):
    if request.method == 'GET':
        studio = get_object_or_404(Studio, id=id)
        studio = studio.__dict__
        studio.pop('_state')
        return JsonResponse(studio)
