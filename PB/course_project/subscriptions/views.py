from django.shortcuts import render
import json
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView

from .models import Subscriptions, Card, Payment, UserSub
from .serializers import SubscriptionSerializer, CardSerializer, UserSubSerializer, PaymentSerializer

# Create your views here.

class AddCard(generics.CreateAPIView):
    """Create a card view to allow creation of a new card instance"""
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def post(self, request, *args, **kwargs):
        """Post method to send data of a specific card"""

        serializer = CardSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_200_OK})

        return Response({'error': "Card not valid."}, status= status.HTTP_400_BAD_REQUEST)

class UpdateCard(generics.UpdateAPIView):
    """Allows user to update their card information"""
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer
    lookup_field = 'user_id'
    
    def put(self, request, pk = None, *args, **kwargs):
        """Put method to allow users to update their card information"""

        # check and see if card exists
        if self.get_object():
            card = self.get_object()
            
            serializer = CardSerializer(card, data=request.data)
            
            if serializer.is_valid():
                serializer.save()

                # change user card to match this one, if user already has subscription
                if UserSub.objects.filter(user_id = self.request.user.id).exists():
                    user_sub = UserSub.objects.get(user_id = self.request.user.id)
                    user_sub.card = self.get_object()
                    user_sub.save()
                        
                return Response(serializer.data, status= status.HTTP_200_OK)
            else:
                return Response({"message": "failed", "details": serializer.errors})
        
        return Response({'error': "Card does not exist."}, status= status.HTTP_400_BAD_REQUEST)

class CardViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CardSerializer

    def get_object(self):
        return Card.objects.get(user_id = self.request.user)

    def get(self, arg):
        serializer = CardSerializer(self.get_object())
        return Response(serializer.data)

class AddSubscription(generics.CreateAPIView):
    """Create a User-Subscription pairing"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSubSerializer

    def post(self, request, *args, **kwargs):
        """Post method to send data for User-Subscription pairing"""

        serializer = UserSubSerializer(data=request.data, context={'request': request})

        # checks to see if user has a card registered
        if not Card.objects.filter(user_id = self.request.user.id).exists():
            return Response({'error': "Cannot add subscription as user has no registered card"})

        # check to see if card is user's
        card_id = request.data.get('card', '')

        card = Card.objects.get(id = card_id)

        if card.user_id != self.request.user.id:
            return Response({'error': "Cannot add subscription as card is not user's."})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            # already 'charge' card
            payment = PaymentSerializer(data=request.data)

            if payment.is_valid(raise_exception=True):
                payment.save()

        return Response({'status': status.HTTP_200_OK})

class UpdateSubscription(generics.UpdateAPIView):
    """Allows user to update their subscription"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSubSerializer
    queryset = UserSub.objects.all()
    lookup_field = 'user_id'
    
    def put(self, request, *args, **kwargs):
        """Put method to allow users to update their subscription"""

        # check and see if usersub exists
        if self.get_object():
            usersub_object = self.get_object()
            
            serializer = UserSubSerializer(usersub_object, data=request.data)

             # check if user is authenticated
            if self.request.user.id == usersub_object.user_id:
                
                # checks to see if user has a card registered
                if not Card.objects.filter(user_id = self.request.user.id).exists():
                    return Response({'error': "Cannot add subscription as user has no registered card"})

                # check to see if card is user's
                card_id = request.data.get('card', '')

                card = Card.objects.get(id = card_id)

                if card.user_id != self.request.user.id:
                    return Response({'error': "Cannot add subscription as card is not user's."})
                
                # if everything is alright, save and return 200 response
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status= status.HTTP_200_OK)
                else:
                    return Response({"message": "failed", "details": serializer.errors})
            else:
                return Response({'error': 'Unauthenticated'})
        
        return Response({'error': "UserSub does not exist."}, status= status.HTTP_400_BAD_REQUEST)

class SubscriptionsViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = Subscriptions

    def get(self, arg):
        subs = Subscriptions.objects.all()
        serilizer = SubscriptionSerializer(subs, many=True)
        return Response(serilizer.data)

class UserSubViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSub


    def get_object(self):
        return UserSub.objects.get(user_id = self.request.user.id)

    def get(self, arg):
        serializer = UserSubSerializer(self.get_object())
        return Response(serializer.data)

class PaymentHistory(APIView):
    """View for payment history of logged in user"""
    serializer_class = PaymentSerializer
    permission_classes =  [IsAuthenticated]

    def get(self, arg):
        """Get method for payment history for logged in user"""

        # checks to see if user has payments made
        if not Payment.objects.filter(user =self.request.user).exists():
            return Response('NOT FOUND', status=404)

        payments = Payment.objects.filter(user = self.request.user)

        # serializer = PaymentSerializer(payments, many=True)

        # return Response(serializer.data)

        # paymentnumber = 1

        payments_json = []

        # append list with previous payments made in JSON format
        for payment in payments:
            dict = {'user': payment.user.__str__(), 'date': payment.date, 'card': payment.card.__str__(), 'sub': payment.subscription.__str__()}
            payments_json.append(dict)

        # section checks to see if user will renew subscription, if so add future upcoming payment

        user = UserSub.objects.get(user=self.request.user)

        if user.DoesNotExist:
            if user.renew:
                if user.subscription.charge_every == 'Month':
                    next_payment = {'user': user.user.__str__(), 'date': user.renew_date + relativedelta(months=+1), 'card': user.card.__str__(), 'sub': user.subscription.__str__()}
                else:
                    next_payment = {'user': user.user.__str__(), 'date': user.renew_date + relativedelta(months=+12), 'card': user.card.__str__(), 'sub': user.subscription.__str__()}
                payments_json.append(dict)

        return JsonResponse(payments_json, safe=False)
