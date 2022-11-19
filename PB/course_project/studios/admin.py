from django.contrib import admin
from .models import Studio, AmenitySet, Amenity, ImageSet, Image

<<<<<<< HEAD
=======

>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
# Register your models here.


class AmenitiesInline(admin.TabularInline):
    model = Studio.amenities.through


class ImagesInline(admin.TabularInline):
    model = Studio.images.through


class StudioAdmin(admin.ModelAdmin):
    inline = [AmenitiesInline, ImagesInline]

    class Meta:
        model = Studio

<<<<<<< HEAD
=======

>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
admin.site.register(Studio, StudioAdmin)
admin.site.register(AmenitySet)
admin.site.register(Amenity)
admin.site.register(ImageSet)
admin.site.register(Image)
