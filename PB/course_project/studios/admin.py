from django.contrib import admin
from .models import Studio, AmenitySet, Amenity, ImageSet, Image


# Register your models here.


class AmenitiesInline(admin.TabularInline):
    model = Studio.amenities.through


class ImagesInline(admin.TabularInline):
    model = Studio.images.through


class StudioAdmin(admin.ModelAdmin):
    inline = [AmenitiesInline, ImagesInline]

    class Meta:
        model = Studio


admin.site.register(Studio, StudioAdmin)
admin.site.register(AmenitySet)
admin.site.register(Amenity)
admin.site.register(ImageSet)
admin.site.register(Image)
