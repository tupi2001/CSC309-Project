from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Studio
import json
from haversine import haversine, Unit
import decimal
from rest_framework import generics, viewsets
import haversine as hs
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from studios.models import Amenities, Images, Studio
from studios.serializers import DistanceSerializer, StudioInfoSerializer

class StudioInformationView(generics.GenericAPIView):
    serializer_class = StudioInfoSerializer
    permission_classes = [AllowAny,]

    def get(self, request, studio_id):
        if not Studio.objects.filter(id=studio_id).exists():
            return Response('NOT FOUND', status=404)

        else:
            studio = Studio.objects.get(id=studio_id)

            amenities_list = []
            amenities = Amenities.objects.filter(studio=studio_id).all()
            for element in amenities:
                dict = {'type': element.type,
                        'quantity':element.quantity}

                amenities_list.append(dict)

            images_list = []
            images = Images.objects.filter(studio=studio_id).all()

            for element in images:
                dict = {
                    'images':element.image.url
                }
                images_list.append(dict)

            data = {
                'name': studio.name,
                'address': studio.address,
                'latitude': studio.latitude,
                'longitude': studio.longitude,
                'postal_code': studio.postal_code,
                'phone_number': studio.phone_number,
                'amenities': amenities_list,
                'images': images_list,
            }
            return Response(data)


class ListDistanceView(generics.GenericAPIView):
    serializer_class = DistanceSerializer
    permission_classes = [AllowAny,]

    def post(self, request):
        lat = decimal.Decimal(float(request.POST.get('latitude')))
        lon = decimal.Decimal(float(request.POST.get('longitude')))

        distance = []
        user_location = (lat, lon)

        for studio in Studio.objects.all():
            studio_location = (studio.latitude, studio.longitude)
            calculated_distance = hs.haversine(user_location, studio_location)
            distance.append(calculated_distance)

        sorted_studios = [x for _, x in sorted(zip(distance, Studio.objects.all()))]
        studio_ordered = []

        for i in range(len(sorted_studios)):
            dict = {
                'name': sorted_studios[i].name,
                'distance': sorted_studios[i]
            }
            studio_ordered.append(dict)
        data = {'studio': studio_ordered}
        return Response(data)

class AllStudioInfoView(generics.ListAPIView):
    queryset = Studio.objects.all()
    permission_classes = [AllowAny,]

    def get_queryset(self):
        queryset = Studio.objects.all()
        name = self.request.query_params.get('name')
        amenities = self.request.query_params.get('amenities')

        if name:
            queryset = queryset.filter(name=name)
        if amenities:
            queryset = queryset.filter(amenities=amenities)

        return queryset



# @api_view(['POST'])
#
# def AllStudios(request):
#     if request.method == 'POST':
#         payload = json.loads(request.body)
#
#         user_latitude = payload.get('latitude', '')
#         user_longitude = payload.get('longitude', '')
#
#         if user_latitude == '' or user_longitude == '':
#             raise ValidationError
#
#         studio_query = Studio.objects.all()
#         response = {}
#         studios = []
#
#         for element in studio_query:
#             studio = element.__dict__
#             studio.pop('_state')
#
#             url_destination = studio['address'].replace(' ', '+') + '+' + studio['postal'].replace('', '+')
#
#             url = "http://maps.google.com/maps/dir/" + str(user_latitude) + ",+" + str(user_longitude) + "/" + url_destination
#
#             latitude_difference = abs(studio['latitude'] - user_latitude) * 111.1
#             longitude_difference = abs(studio['longitude'] - user_longitude) * 111.1
#
#             distance = math.sqrt(latitude_difference ** 2 + longitude_difference ** 2)
#             studio['distance'] = round(distance, 2)
#
#             studio.pop('latitude')
#             studio.pop('longitude')
#             studio.pop('phone_number')
#             studio.pop('postal')
#             studio['directions'] = url
#
#             studios.append(studio)
#
#         studios = sorted(studios, key=lambda d: d['distance'])
#
#
#         for element in studios:
#             response[element['name']] = element
#
#         return JsonResponse(response)
#
# @api_view(['GET'])
# def StudioInformation(request, id):
#     print(id)
#     if request.method == 'GET':
#         studio = get_object_or_404(Studio, id=id)
#         print(studio)
#         studio = studio.__dict__
#         studio.pop('_state')
#         return JsonResponse(studio)
