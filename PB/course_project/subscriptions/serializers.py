from .models import Subscriptions, Card, Payment, UserSub, DURATION
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ('value', 'charge_every')


class CardSerializer(serializers.ModelSerializer):
    user = CurrentUserDefault

    class Meta:
        model = Card
        fields = ('user', 'name', 'card')

    def validate_card(self, data):
        card = data

        if len(card) != 23:
            raise serializers.ValidationError("Card must have 23 digits in total.")

        return card

    def create(self, validated_data):
        card = Card(user = CurrentUserDefault, name = validated_data['name'], card = validated_data['card'])
        card.save()
        return card

    
class PaymentSerializer(serializers.ModelSerializer):
    user = CurrentUserDefault
    subscription = SubscriptionSerializer(source='subscription')

    class Meta:
        model = Payment
        fields = ('user', 'subscription', 'card')

class UserSubSerializer(serializers.ModelSerializer):
    user = CurrentUserDefault
    subscription = SubscriptionSerializer(source='subscription')

    class Meta:
        model = UserSub
        fields = ('user', 'subscription', 'card_information', 'active', 'renew')
