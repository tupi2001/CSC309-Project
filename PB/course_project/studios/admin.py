from django.contrib import admin
from .models import Studio, Amenities, Images

# admin can create a new studio, add amenities or images
admin.site.register(Studio)
admin.site.register(Amenities)
admin.site.register(Images)
