from django.db import models
from django.db.models import CASCADE
from studios.models import Studio
from accounts.models import CustomUser
from recurrence.fields import RecurrenceField

class Class(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, 
        default=1, null=False)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=200, null=False)
    keywords = models.CharField(max_length=200, null=False)  # how to create a list
    capacity = models.PositiveIntegerField(null=False)
    recurrences = RecurrenceField(null=True)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    # end_date = models.DateField(null=False)
    # users = models.ManyToManyField(CustomUser, default=1)

    def __str__(self):
        return self.name


class UserAndClass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, default=1)
    gym_class = models.ForeignKey(Class, on_delete=CASCADE, default=1)