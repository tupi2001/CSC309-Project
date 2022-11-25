from django.contrib import admin
from subscriptions.models import UserSub, Subscriptions, Card

# admin can create a new studio, add amenities or images
admin.site.register(Card)
admin.site.register(Subscriptions)
admin.site.register(UserSub)
