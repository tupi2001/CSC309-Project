from django.contrib import admin
from .models import Studio, Amenities, Images

# Register your models here.


# class AmenitiesInline(admin.TabularInline):
#     model = Studio.amenities.through
#
#
# class ImagesInline(admin.TabularInline):
#     model = Studio.images.through
#
#
# class StudioAdmin(admin.ModelAdmin):
#     inline = [AmenitiesInline, ImagesInline]
#
#     class Meta:
#         model = Studio

admin.site.register(Studio)
# admin.site.register(AmenitySet)
admin.site.register(Amenities)
# admin.site.register(ImageSet)
admin.site.register(Images)
