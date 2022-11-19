from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

<<<<<<< HEAD
=======

>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
# Create your models here.

class Amenity(models.Model):
    type = models.CharField(max_length=30, null=False)

    def __str__(self):
        return str(self.type)

<<<<<<< HEAD
class Image(models.Model):
    image = models.ImageField(upload_to = 'studios/images')
=======

class Image(models.Model):
    image = models.ImageField(upload_to='studios/images')
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18

    def __str__(self):
        return str(self.image)

<<<<<<< HEAD
class Studio(models.Model):
    name = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=200, null = False)
=======

class Studio(models.Model):
    name = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=200, null=False)
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)], null=False
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)], null=False
    )
    postal = models.CharField(max_length=7, null=False)
    phone_number = models.PositiveIntegerField(
<<<<<<< HEAD
        validators=[MaxValueValidator(9999999999)], null = False
    )
    images = models.ManyToManyField(Image, related_name='ImageSet', blank = True, through='ImageSet')
    amenities = models.ManyToManyField(
        Amenity, related_name='AmenitySet', blank = True, through='AmenitySet'
=======
        validators=[MaxValueValidator(9999999999)], null=False
    )
    images = models.ManyToManyField(Image, related_name='ImageSet', blank=True, through='ImageSet')
    amenities = models.ManyToManyField(
        Amenity, related_name='AmenitySet', blank=True, through='AmenitySet'
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
    )

    def __str__(self):
        return str(self.name)


class AmenitySet(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True)
<<<<<<< HEAD
    type = models.ForeignKey(Amenity, on_delete = models.CASCADE, null=True)
=======
    type = models.ForeignKey(Amenity, on_delete=models.CASCADE, null=True)
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
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
