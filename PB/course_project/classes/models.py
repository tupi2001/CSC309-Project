from django.db import models
from django.db.models import CASCADE
from studios.models import Studio
from accounts.models import CustomUser
from recurrence.fields import RecurrenceField

from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
import datetime
from datetime import date

class Class(models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, 
        default=1, null=False)
    name = models.CharField(max_length=15, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=15, null=False)
    keywords = models.CharField(max_length=200, null=False)  # how to create a list
    capacity = models.PositiveIntegerField(null=False)
    # recurrences = RecurrenceField(null=True)
    frequency = models.CharField(max_length=15, null=True)
    weekday = models.CharField(max_length=2, null=True)
    start_date = models.CharField(max_length=9, null=True)
    end_date = models.CharField(max_length=9, null=True)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    date = models.DateTimeField(default=date.today())
    # end_date = models.DateField(null=False)
    # users = models.ManyToManyField(CustomUser, default=1)

    def __str__(self):
        return self.name

    def frequency(self):
        if self.frequency not in {YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY}:
            raise ValueError('Please enter a valid frequency')
        if self.weekday not in {MO, TU, WE, TH, FR, SA, SU}:
            raise ValueError('Please enter a valid weekday')

        start = self.start_date
        date_format = '%m/%d/%Y'
        try:
            datetime.datetime.strptime(start, date_format)
        except ValueError:
            raise ValueError('Please enter a valid date')
        start_date = datetime.strptime(start, '%m/%d/%y')

        end = self.end_date
        date_format = '%Y/%m/%d'
        try:
            datetime.datetime.strptime(end, date_format)
        except ValueError:
            raise ValueError('Please enter a valid date')
        end_date = datetime.strptime(end, '%m/%d/%y')
        count = relativedelta(start_date, end_date).weeks

        dates = list(rrule(self.frequency, count=count, byweekday=self.weekday, dtstart=start_date))
        return dates


        


class UserAndClass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, default=1)
    gym_class = models.ForeignKey(Class, on_delete=CASCADE, default=1)