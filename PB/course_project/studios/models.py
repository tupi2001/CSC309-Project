from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import re
from django.db.models import CASCADE
from django.forms import forms
from rest_framework.exceptions import ValidationError

# Create your models here.
class Studio(models.Model):
    name = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=200, null = False)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], null=False
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], null=False
    )
    postal_code = models.CharField(max_length=7, null=False)
    phone_number = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999)], null = False
    )

    def __str__(self):
        return self.name

    def clean(self):
        phone_regex = re.compile(
            '^\(?([0-9]{3})\)?[-]?([0-9]{3})[-]?([0-9]{4})$')
        postal_regex = re.compile('[A-Z]{1}[0-9]{1}[A-Z]{1}\s*[0-9]{1}[A-Z]{1}['
                                  '0-9]{1}')
        if not phone_regex.match(self.phone_number):
            raise forms.ValidationError('Phone number invalid')

        if not postal_regex.match(self.postal):
            raise forms.ValidationError('Postal code invalid')

class Amenities(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    type = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.type

class Images(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    image = models.ImageField(null=True)

# class Amenity(models.Model):
#     type = models.CharField(max_length=30, null=False)
#
#     def __str__(self):
#         return str(self.type)
#
# class Image(models.Model):
#     image = models.ImageField(upload_to = 'studios/images')
#
#     def __str__(self):
#         return str(self.image)
#
# class Studio(models.Model):
#     name = models.CharField(max_length=40, null=False)
#     address = models.CharField(max_length=200, null = False)
#     latitude = models.FloatField(
#         validators=[MinValueValidator(-90), MaxValueValidator(90)], null=False
#     )
#     longitude = models.FloatField(
#         validators=[MinValueValidator(-180), MaxValueValidator(180)], null=False
#     )
#     postal = models.CharField(max_length=7, null=False)
#     phone_number = models.PositiveIntegerField(
#         validators=[MaxValueValidator(9999999999)], null = False
#     )
#     images = models.ManyToManyField(Image, related_name='ImageSet', blank = True, through='ImageSet')
#     amenities = models.ManyToManyField(
#         Amenity, related_name='AmenitySet', blank = True, through='AmenitySet'
#     )
#
#     def __str__(self):
#         return str(self.name)
#
#
# class AmenitySet(models.Model):
#     studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True)
#     type = models.ForeignKey(Amenity, on_delete = models.CASCADE, null=True)
#     quantity = models.PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return str(self.studio) + ': ' + str(self.type) + ' - ' + str(self.quantity)
#
#     class Meta:
#         unique_together = [['studio', 'type']]
#
#
# class ImageSet(models.Model):
#     studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True)
#     image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
#
#     def __str__(self):
#         return str(self.studio) + ': ' + str(self.image)
#
#     class Meta:
#         unique_together = [['studio', 'image']]
