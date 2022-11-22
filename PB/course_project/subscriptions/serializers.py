from .models import Subscriptions, Card, Payment, UserSub, DURATION
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for a subscription"""
    class Meta:
        """Holds the model and its specific fields that will be displayed on the UI"""
        model = Subscriptions
        fields = ('value', 'charge_every')


class CardSerializer(serializers.ModelSerializer):
    """Serializer for a card"""
    class Meta:
        """Holds the model and its specific fields that will be displayed on the UI"""
        model = Card
        fields = ('user', 'name', 'card')

    def validate_card(self, data):
        """Method for validating if card is inputted correctly"""
        card = data

        if len(card) != 23:
            raise serializers.ValidationError("Card must have 23 digits in total.")

        return card

    def create(self, validated_data):
        """Method for creating card instance"""
        card = Card(user = validated_data['user'], name = validated_data['name'], card = validated_data['card'])
        card.save()
        return card

    
class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for a payment"""
    class Meta:
        """Holds the model and its specific fields that will be displayed on the UI"""
        model = Payment
        fields = ('user', 'subscription', 'date', 'card')

class UserSubSerializer(serializers.ModelSerializer):
    """Serializer for a user-subscription relation"""
    user = CurrentUserDefault

    class Meta:
        """Holds the model and its specific fields that will be displayed on the UI"""
        model = UserSub
        fields = ('user', 'subscription', 'card', 'renew')
