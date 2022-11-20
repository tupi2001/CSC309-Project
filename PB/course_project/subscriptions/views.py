from django.shortcuts import render
import jwt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from .forms import CardInformation
from .models import Subscriptions, Card, Payment, UserSub
from .serializers import SubscriptionSerializer, CardSerializer, UserSubSerializer, PaymentSerializer

# Create your views here.

class AddCard(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def post(self, request, *args, **kwargs):
        serializer = CardSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
        
        return Response({'status': status.HTTP_200_OK, 'Token': token.key})

class UpdateCard(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_object(self):
        user_obj = self.request.user.pk

        return get_object_or_404(Card, user=user_obj)

class AddSubscription(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSubSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSubSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
        
        return Response({'status': status.HTTP_200_OK, 'Token': token.key})

class UpdateSubscription(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSubSerializer

    def get_object(self):
        user_obj = self.request.user.pk

        return get_object_or_404(UserSub, user=user_obj)

@api_view(['GET'])
def PaymentHistory(request):
    if request.method == 'GET':
        payment = Payment.objects.filter(user=request.user)
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data)