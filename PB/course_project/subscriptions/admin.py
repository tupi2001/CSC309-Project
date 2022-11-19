from django.contrib import admin
from subscriptions.models import Subscriptions, UserSub, Card, Payment

# Register your models here.

admin.site.register(Subscriptions)
admin.site.register(UserSub)
admin.site.register(Card)
admin.site.register(Payment)