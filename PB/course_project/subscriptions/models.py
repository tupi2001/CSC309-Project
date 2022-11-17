from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

DURATION = (
('Month', 'mon'),
('Year', 'yea')
)

class Subscriptions(models.Model):
    value = models.FloatField()

    charge_every = models.CharField(choices=DURATION, max_length=5, default='Month')

    def __str__(self):
        return str(self.value) + ' per ' + str(self.charge_every)

class Card(models.Model):
    # user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    card = models.CharField(max_length=23, validators=[MinLengthValidator(23)])

    def __str__(self):
        return str(self.card)

class Payments(models.Model):
    # user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    card = models.OneToOneField(Card, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.amount) + ', paid on ' + str(self.date)

class UserSub(models.Model):
    # user = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE)
    subscription = models.OneToOneField(Subscriptions, blank=True, on_delete=models.CASCADE)
    card_information = models.OneToOneField(Card, blank=True, on_delete=models.CASCADE)
    payment_history = models.ForeignKey(to=Payments, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    renew = models.BooleanField(default=False)

    # add user here
    def __str__(self):
        return str(self.active)

