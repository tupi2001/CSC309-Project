from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import re
from django.db.models import CASCADE
from django.forms import forms
from rest_framework.exceptions import ValidationError


class Studio(models.Model):
    """Studios models: introducing model attributes
        Parameters:
            name: name of studio
            address: address of studio
            latitude: latitude of the studio in order to determine distance
            longitude: longitude of the studio in order to determine distance
            postal_code: postal code of studio
    """
    name = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=200, null=False)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], null=False
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], null=False
    )
    postal_code = models.CharField(max_length=7, null=False)
    phone_number = models.CharField(
        max_length=15, null=False
    )

    def __str__(self):
        """function that returns the name of the studio as a string"""
        return self.name

    def clean(self):
        """Checks that the phone number and postal code are in the correct format"""
        phone_regex = re.compile(
            '^\(?([0-9]{3})\)?[-]?([0-9]{3})[-]?([0-9]{4})$')
        postal_regex = re.compile('[A-Z]{1}[0-9]{1}[A-Z]{1}\s*[0-9]{1}[A-Z]{1}['
                                  '0-9]{1}')
        if not phone_regex.match(self.phone_number):
            raise forms.ValidationError('Phone number invalid')

        if not postal_regex.match(self.postal_code):
            raise forms.ValidationError('Postal code invalid')


class Amenities(models.Model):
    """Amenities stored in a Studio
        Parameters:
            studio: studio is a foreign key and holds specific amenities
            type: type of amenities
            quantity: quantity of each amenity
    """
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    type = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        """Returns the type of amenities as a string"""
        return self.type


class Images(models.Model):
    """Images of a specific studio
        Parameters:
            studio: studio is a foreign key and has specific images
            image: images of a studio
    """
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    image = models.ImageField(null=True)
