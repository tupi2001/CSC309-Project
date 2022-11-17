from django.contrib import admin
from .models import Subscriptions, UserSub

# Register your models here.

admin.site.register(Subscriptions)
admin.site.register(UserSub)