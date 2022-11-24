from rest_framework import serializers

from classes.models import GymClass, UserAndClass
from studios.serializers import StudioSerializer
# from accounts.serializers import UserSerializer

from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *
import json


class ClassSerializer(serializers.ModelSerializer):
    """Serializer for creating a class"""
    frequency2 = serializers.CharField()
    class Meta:
        """Fields of a class:
            studio: studio name
            name: class name
            description : class description
            coach: class coach
            keywords: class keywords
            capacity: class capacity
            frequency2: class frequency: YEARLY, MONTHLY, WEEKLY, DAILY
            weekday: class weekday: MO, TU, WE, TH, FR, SA, SU
            start_date: date of first class of this type
            end_date: date of last class of this type
            start_time: class start time
            end_time: class end_time
        """        
        model = GymClass
        fields = ['studio', 'name', 'description', 'coach', 
            'keywords', 'capacity', 'frequency2', 'weekday', 'start_date', 
            'end_date', 'start_time', 'end_time']

    def frequency_validate(self, data):
        """Verify that the user inputted a valid frequency"""
        frequency = data
        if frequency not in {'YEARLY', 'MONTHLY', 'WEEKLY', 'DAILY', 'HOURLY'}:
            # raise ValueError('Please enter a valid frequency')
            raise serializers.ValidationError('Please enter a valid frequency')
        return frequency

    def weekday_validate(self, data):
        """Verify that the user inputted a valid weekday"""
        weekday = data
        if weekday not in {'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'}:
            raise serializers.ValidationError('Please enter a valid weekday')
        return weekday

    def create(self, data):
        """
        Generate recurring classes based on the class and frequency info inputted 
        by the user
        """
        start = data['start_date']
        frequency = data['frequency2']

        if frequency == 'YEARLY':
            freq = YEARLY
        if frequency == 'MONTHLY':
            freq = MONTHLY
        if frequency == 'WEEKLY':
            freq = WEEKLY
        if frequency == 'DAILY':
            freq = DAILY
        if frequency == 'HOURLY':
            freq = HOURLY

        weekday = data['weekday']
        if weekday == 'MO':
            wday = MO
        if weekday == 'TU':
            wday = TU
        if weekday == 'WE':
            wday = WE
        if weekday == 'TH':
            wday = TH
        if weekday == 'FR':
            wday = FR
        if weekday == 'SA':
            wday = SA
        if weekday == 'SU':
            wday = SU

        date_format = '%m/%d/%Y'
        try:
            datetime.strptime(start, date_format)
        except ValueError:
            raise ValueError('Please enter a valid date')
        start_date = datetime.strptime(start, '%m/%d/%Y')
        end = data['end_date']
        try:
            datetime.strptime(end, date_format)
        except ValueError:
            raise serializers.ValidationError('Please enter a valid date')
        end_date = datetime.strptime(end, '%m/%d/%Y')
        count = abs(relativedelta(start_date, end_date).weeks) + 1  # number of recurring classes there should be

        dates = list(rrule(freq=freq, count=count, byweekday=wday, dtstart=start_date))

        created_classes = []
        for date in dates:
            gym_class = GymClass.objects.create(
                studio=data['studio'],
                name=data['name'],
                description=data['description'],
                keywords=data['keywords'],
                capacity=data['capacity'],
                # frequency=data['frequency'], 
                weekday=data['weekday'], 
                start_date=data['start_date'],
                start_time=data['start_time'],
                end_time=data['end_time'],
                end_date=data['end_date'],
                date=date  
            )
            gym_class.save()
            entry = {'name': gym_class.name, 'studio': gym_class.studio, 'id': gym_class.id, 
                'start_date': date}
            created_classes.append(entry)
            
        return gym_class
    
    # def default(self):
    #     """Returns a class in JSON format"""
    #     return json.dumps(self.__dict__)

class UserAndClassSerializer(serializers.ModelSerializer):
    # classes = ClassSerializer()
    # users = UserSerializer()

    class Meta:
        model = UserAndClass
        fields = ['user', 'gym_class']

    def create(self, data):
        userandclass = UserAndClass.objects.create(
            user=data['user'],
            gym_class=data['gym_class'],
        )
        userandclass.save()

        return userandclass
