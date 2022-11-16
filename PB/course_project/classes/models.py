from django.db import models
from django.db.models import CASCADE
from studios.models import Studio

class Class(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=200, null=False)
    keywords = models.CharField(max_length=200, null=False)  # how to create a list
    capacity = models.PositiveIntegerField(null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    end_date = models.DateField(null=False)

    def __str__(self):
        return self.name
