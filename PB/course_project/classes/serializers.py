from rest_framework import serializers

from classes.models import Class, UserAndClass
from studios.serializers import StudioSerializer
from accounts.serializers import UserSerializer

from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
import datetime


class ClassSerializer(serializers.ModelSerializer):
    studio = StudioSerializer()

    class Meta:
        model = Class
        fields = ['id', 'studio', 'name', 'description', 'coach', 
            'keywords', 'capacity', 'start_time', 'end_time']

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
        try:
            datetime.datetime.strptime(end, date_format)
        except ValueError:
            raise ValueError('Please enter a valid date')
        end_date = datetime.strptime(end, '%m/%d/%y')
        count = relativedelta(start_date, end_date).weeks  # number of recurring classes there should be

        dates = list(rrule(self.frequency, count=count, byweekday=self.weekday, dtstart=start_date))
        return dates

    def create(self, data):
        dates = self.frequency()

        for date in dates:
            gym_class = Class.objects.create(
                studio = data['studio'],
                name=data['name'],
                description=data['description'],
                keywords=data['keywords'],
                capacity=data['capacity'],
                frequency=data['frequency'], 
                weekday=data['weekday'], 
                start_date=data['start_date'],
                end_date=data['end_date'],
                date=date  
            )
            gym_class.save()
        return

class UserAndClassSerializer(serializers.ModelSerializer):
    classes = ClassSerializer()
    users = UserSerializer()

    class Meta:
        model = UserAndClass
        fields = ['class', 'users']