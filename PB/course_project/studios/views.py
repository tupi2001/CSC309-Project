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
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from studios.models import Amenities, Images, Studio
from studios.serializers import DistanceSerializer, StudioSerializer

class StudioInformationView(generics.GenericAPIView):
    """View for studio information"""
    serializer_class = StudioSerializer
    permission_classes = [AllowAny,]

    def get(self, request, studio_id):
        """Get method for studio information"""

        # if the studio with the specific id does not exist return a 404 response
        if not Studio.objects.filter(id=studio_id).exists():
            return Response('NOT FOUND', status=404)
        # create a json response with the data of the specific studio
        else:
            # get specific studio
            studio = Studio.objects.get(id=studio_id)

            # the list that will hold the json string
            amenities_list = []
            # get all amenities
            amenities = Amenities.objects.filter(studio=studio_id).all()
            # for every amenity in amenities assign its type and quantity as a dictionary for the
            # JSON string
            for element in amenities:
                dict = {'type': element.type,
                        'quantity':element.quantity}

                amenities_list.append(dict)

            # repeat the process for amenities for images
            images_list = []
            images = Images.objects.filter(studio=studio_id).all()

            for element in images:
                images_list.append(element.image.url)

            # create JSON string for the entire studio using the images and amenities json string
            # provided
            data = {
                'id': studio.id,
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
    """Lists the distances of studios from closest to furthest"""
    serializer_class = DistanceSerializer
    permission_classes = [AllowAny,]

    def post(self, request):
        """function to find the location using latitude and longitude of multiple studios and
        return them in order of the closest to the furthest"""
        print(request.POST)
        lat = decimal.Decimal(float(request.POST.get('latitude')))
        lon = decimal.Decimal(float(request.POST.get('longitude')))

        # creating json string
        distance = []
        user_location = (lat, lon)
        # for every studio use the latitude and longitude to find the location using haversine
        # formula
        for studio in Studio.objects.all():
            studio_location = (studio.latitude, studio.longitude)
            calculated_distance = hs.haversine(user_location, studio_location)
            distance.append(calculated_distance)

        # sort the studios by which is closest and which is furthest
        sorted_studios = [x for _, x in sorted(zip(distance, Studio.objects.all()))]
        studio_ordered = []

        # create a json string using the name of the studios and the ordered list
        for i in range(len(sorted_studios)):
            amenities_list = []
            # get all amenities
            amenities = Amenities.objects.filter(studio=sorted_studios[i].id).all()
            # for every amenity in amenities assign its type and quantity as a dictionary for the
            # JSON string
            for element in amenities:
                dict = {'type': element.type,
                        'quantity':element.quantity}

                amenities_list.append(dict)
            dict = {
                'id': sorted_studios[i].id,
                'name': sorted_studios[i].name,
                'latitude': sorted_studios[i].latitude,
                'longitude': sorted_studios[i].longitude,
                'amenities': amenities_list,
                'phone_number': sorted_studios[i].phone_number,
                'distance': distance[i],
            }
            studio_ordered.append(dict)
        # return the the studio with values of name and distance
        data = {'studio': studio_ordered}
        return Response(data)

class AllStudioInfoView(generics.ListAPIView):
    """Tentative Search function"""
    serializer_class =  StudioSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        """Returns a specific gym a user looks for by name or amenities"""
        queryset = Studio.objects.all()
        name = self.request.query_params.get('name')
        amenities = self.request.query_params.get('amenities')
        id = self.request.query_params.get('id')

        if name:
            queryset = queryset.filter(name=name)
        if amenities:
            queryset = queryset.filter(amenities=amenities)
        if id:
            queryset = queryset.filter(id=id)

        return queryset
