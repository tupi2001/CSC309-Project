from django.core.validators import MinLengthValidator
from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from accounts.models import CustomUser

# Create your models here.

DURATION = (
('Month', 'mon'),
('Year', 'yea')
)

class Subscriptions(models.Model):
    """Subscriptions models: model for subscriptions
        Parameters:
            value: value of subscription
            charge_every: how often to charge user
    """
    value = models.FloatField(null=False)

    charge_every = models.CharField(choices=DURATION, max_length=5, default='Month')

    def __str__(self):
        """function that returns model as a string"""
        return str(self.value) + ' per ' + str(self.charge_every)

class Card(models.Model):
    """Card linked to a specific user
        Parameters:
            user: user linked to this card
            name: name on card
            card: card number (including expiration date and cvv)
    """
    user = models.OneToOneField(to=CustomUser, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    card = models.CharField(max_length=23, validators=[MinLengthValidator(23)], null=False)

    def __str__(self):
        """function that returns model as a string"""
        return str(self.card)

class Payment(models.Model):
    """Individual payments from a given individual for a given subscripion
        Parameters:
            user: user linked to this payment
            subscription: type of subscription
            date: when payment was made
            card: which card instance was used
    """
    user = models.ForeignKey(to=CustomUser, null=False, on_delete=models.CASCADE)
    subscription = models.ForeignKey(to=Subscriptions, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=False)

    def __str__(self):
        """function that returns model as a string"""
        return str(self.subscription.value) + ', paid on ' + str(self.date)

class UserSub(models.Model):
    """Model that links user to a subscription
        Parameters:
            user: custom_user object
            subscription: type of subscription currently assigned to user
            card: card linked to user, which will be charged
            active: if the subscription is currently active, ongoin
            renew: if the card should be charged again next billing cycle
            renew_date: when the card should be charged once again
    """
    user = models.OneToOneField(to=CustomUser, null=False, on_delete=models.CASCADE, unique=True)
    subscription = models.ForeignKey(Subscriptions, blank=True, on_delete=models.CASCADE)
    card = models.OneToOneField(Card, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    renew = models.BooleanField(default=False)
    renew_date = models.DateTimeField(auto_now_add=True)

    def renew_required(self):
        """function that checks if card needs to be charged"""

        if date.today >= self.renew_date:
            if self.renew:
                # charge card in theory
                Payment.objects.create(user=self.user, subscription=self.subscription, date=date.today, card=self.card)

                if self.subscription.charge_every == 'Month':
                    self.renew_date = date.today + relativedelta(months=+1)
                else:
                    self.renew_date = date.today + relativedelta(years=1)

                self.save()

                return True

            self.active = False
            return False

    def __str__(self):
        """function that returns model as a string"""
        return str(self.user.__str__) + ' ' + str(self.subscription.__str__)

