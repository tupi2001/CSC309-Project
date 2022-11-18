from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class Amenity(models.Model):
    type = models.CharField(max_length=30, null=False)

    def __str__(self):
        return str(self.type)


class Image(models.Model):
    image = models.ImageField(upload_to='studios/images')

    def __str__(self):
        return str(self.image)


class Studio(models.Model):
    name = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=200, null=False)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], null=False
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], null=False
    )
    postal = models.CharField(max_length=7, null=False)
    phone_number = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999999999)], null=False
    )
    images = models.ManyToManyField(Image, related_name='ImageSet', blank=True, through='ImageSet')
    amenities = models.ManyToManyField(
        Amenity, related_name='AmenitySet', blank=True, through='AmenitySet'
    )

    def __str__(self):
        return str(self.name)


class AmenitySet(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(Amenity, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.studio) + ': ' + str(self.type) + ' - ' + str(self.quantity)

    class Meta:
        unique_together = [['studio', 'type']]


class ImageSet(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.studio) + ': ' + str(self.image)

    class Meta:
        unique_together = [['studio', 'image']]
