from django.core.validators import MinLengthValidator
from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta


# Create your models here.

DURATION = (
('Month', 'mon'),
('Year', 'yea')
)

class Subscriptions(models.Model):
    value = models.FloatField(null=False)

    charge_every = models.CharField(choices=DURATION, max_length=5, default='Month')

    def __str__(self):
        return str(self.value) + ' per ' + str(self.charge_every)

    def create_subscription(self, value, charge_every):
        if not value or not charge_every:
            raise ValueError('This is a required field')

        subscription = self.model(value=value, charge_every=charge_every)
        subscription.save(using=self.db)
        return subscription

class Card(models.Model):
    # user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    card = models.CharField(max_length=23, validators=[MinLengthValidator(23)], null=False)

    def __str__(self):
        return str(self.card)

class Payment(models.Model):
    # user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    subscription = models.OneToOneField(Subscriptions, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    card = models.OneToOneField(Card, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.subscription.value) + ', paid on ' + str(self.date)

class UserSub(models.Model):
    # user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    subscription = models.OneToOneField(Subscriptions, blank=True, on_delete=models.CASCADE)
    card_information = models.OneToOneField(Card, blank=True, on_delete=models.CASCADE)
    payment_history = models.ForeignKey(to=Payment, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    renew = models.BooleanField(default=False)
    renew_date = models.DateTimeField(auto_now_add=True)

    def renew_required(self):

        if date.today >= self.renew_date:
            if self.renew:
                if self.subscription.charge_every == 'Month':
                    self.renew_date = date.today + relativedelta(months=+1)
                if self.subscription.charge_every == 'Year':
                    self.renew_date = date.today + relativedelta(years=1)
                
                # charge card in theory

                return True

            self.active = False
            return False

    # add user here
    def __str__(self):
        return str(self.active)

