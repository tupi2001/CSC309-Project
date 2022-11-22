from django.shortcuts import render
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dateutil.relativedelta import relativedelta

from .models import Subscriptions, Card, Payment, UserSub
from .serializers import SubscriptionSerializer, CardSerializer, UserSubSerializer, PaymentSerializer

# Create your views here.

class AddCard(generics.CreateAPIView):
    """Create a card view to allow creation of a new card instance"""
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def post(self, request, *args, **kwargs):
        """Post method to send data of a specific card"""
        card = self.get_object()

        serializer = CardSerializer(data=request.data, context={'request': request})

        # checks to see if logged in user matches user the card is being registered to
        if self.request.user.id == card.user_id:
            if serializer.is_valid():
                serializer.save()
        else:
            return Response({'error': 'Unauthenticated'})

        return Response({'status': status.HTTP_200_OK})

class UpdateCard(generics.UpdateAPIView):
    """Allows user to update their card information"""
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self, pk):
        """Override to seek users by user_id"""
        return self.get_serializer().Meta.model.objects.get(user_id = pk)
    
    def put(self, request, pk = None, *args, **kwargs):
        """Put method to allow users to update their card information"""

        # check and see if card exists
        if self.get_queryset(pk):
            card = self.get_queryset(pk)
            
            serializer = CardSerializer(self.get_queryset(pk), data=request.data)
            
            # check if user is authenticated
            if self.request.user.id == card.user_id:
                if serializer.is_valid():
                    serializer.save()

                # change user card to match this one, if user already has subscription
                if UserSub.objects.filter(user_id = self.request.user.id).exists():
                    user_sub = UserSub.objects.get(user_id = self.request.user.id)
                    user_sub.card = self.get_object()
                    user_sub.save()
                        
                return Response(serializer.data, status= status.HTTP_200_OK)
            else:
                return Response({'error': 'Unauthenticated'})
        
        return Response({'error': "Card does not exist."}, status= status.HTTP_400_BAD_REQUEST)

class AddSubscription(generics.CreateAPIView):
    """Create a User-Subscription pairing"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSubSerializer

    def post(self, request, *args, **kwargs):
        """Post method to send data for User-Subscription pairing"""
        usersub_object = self.get_object()

        serializer = UserSubSerializer(data=request.data, context={'request': request})

        # checks to see if card being used is user's
        if not usersub_object.card_id == self.request.user.id:
            return Response({'error': "Cannot add card as it does not belong to current user"})

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

    def get_queryset(self, pk):
        """Override to seek users by user_id"""
        return self.get_serializer().Meta.model.objects.get(user_id = pk)
    
    def put(self, request, pk = None, *args, **kwargs):
        """Put method to allow users to update their subscription"""

        # check and see if usersub exists
        if self.get_queryset(pk):
            usersub_object = self.get_object()
            
            serializer = UserSubSerializer(self.get_queryset(pk), data=request.data)

             # check if user is authenticated
            if self.request.user.id == usersub_object.user_id:
                
                # checks to see if card being used is user's
                if not usersub_object.card_id == self.request.user.id:
                    return Response({'error': "Cannot add card as it does not belong to current user"})
                
                # if everything is alright, save and return 200 response
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status= status.HTTP_200_OK)
            else:
                return Response({'error': 'Unauthenticated'})
        
        return Response({'error': "UserSub does not exist."}, status= status.HTTP_400_BAD_REQUEST)


class PaymentHistory(generics.GenericAPIView):
    """View for payment history of logged in user"""
    serializer_class = PaymentSerializer
    permission_classes =  [IsAuthenticated]

    def get(self, *args, **kwargs):
        """Get method for payment history for logged in user"""

        # checks to see if user has payments made
        if not Payment.objects.filter(user=self.request.user).exists():
            return Response('NOT FOUND', status=404)

        payments = Payment.objects.filter(user = self.request.user)

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
                    next_payment = {'user': user.user.__str__(), 'date': user.renew_date + relativedelta(years=+1), 'card': user.card.__str__(), 'sub': user.subscription.__str__()}
                payments_json.append(next_payment)

        data = {'payments': payments_json}

        return JsonResponse(data)