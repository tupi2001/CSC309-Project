from django.contrib import admin
from subscriptions.models import Subscriptions, UserSub, Card, Payment

# admin can create/edit subscription types, can register/edit a subscription to a given user, 
# can add/edit user cards and add/edit user payments

admin.site.register(Subscriptions)
admin.site.register(UserSub)
admin.site.register(Card)
admin.site.register(Payment)