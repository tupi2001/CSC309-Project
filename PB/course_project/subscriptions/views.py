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

from .models import Subscriptions, Card, Payment, UserSub
from .serializers import SubscriptionSerializer, CardSerializer, UserSubSerializer, PaymentSerializer

# Create your views here.

class AddCard(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def post(self, request, *args, **kwargs):
        serializer = CardSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        
        return Response({'status': status.HTTP_200_OK})

class UpdateCard(generics.UpdateAPIView):
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def patch(self, request, *args, **kwargs):
        card_object = self.get_object()
        # data = request.data

        serializer = self.get_serializer(card_object, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})

        if card_object.user == self.request.user:
            card_object.name = data.get('name', card_object.name)
            card_object.card = data.get('card', card_object.card)

            card_object.save()
            serializer = CardSerializer(card_object)
            return Response(serializer.data)

        return Response({'error': 'Unauthenticated'})

class AddSubscription(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSubSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = UserSubSerializer(data=data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            payment = PaymentSerializer(data=data)

            if payment.is_valid(raise_exception=True):
                payment.save()

        return Response({'status': status.HTTP_200_OK})

class UpdateSubscription(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSubSerializer

    def patch(self, request, *args, **kwargs):
        sub_object = self.get_object()
        data = request.data

        if sub_object.user == self.request.user:
            sub_object.name = data.get('subscription', sub_object.subscription)
            sub_object.card = data.get('card_information', sub_object.card_information)
            sub_object.renew = data.get('renew', sub_object.renew)

            sub_object.save()
            serializer = UserSubSerializer(sub_object)
            return Response(serializer.data)

        return Response({'error': 'Unauthenticated'})

class PaymentHistory(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes =  [IsAuthenticated]
    search_fields = ('user')
    paginate_by = 20

    def get_queryset(self):
        if not Payment.objects.filter(user=self.request.user).exists():
            return Response('NOT FOUND', status=404)

        payments = Payment.objects.filter(user = self.request.user)

        payments_dict = {}

        i = 1

        for payment in payments:
            object = payments.get(id=i)
            payments_dict[object.date] = [object.user, object.card, object.subscription]

        return payments