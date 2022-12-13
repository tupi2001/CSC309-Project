from django.db import models
from django.db.models import CASCADE
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from studios.models import Studio
from accounts.models import CustomUser

from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
import datetime
from datetime import date
import json

class GymClass(models.Model):
    """Model that holds the attributes of a class
        studio: studio name
        name: class name
        description : class description
        coach: class coach
        keywords: class keywords
        capacity: class capacity
        current_capacity: current capacity of class, changes when user enrols in class
        frequency2: class frequency: YEARLY, MONTHLY, WEEKLY, DAILY
        weekday: class weekday: MO, TU, WE, TH, FR, SA, SU
        date_created: date that instance(s) were created
        end_date: date of last class of this type
        start_time: class start time
        end_time: class end_time
        date: date of class instance
    """
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, 
        default=1, null=False)
    name = models.CharField(max_length=15, null=False)
    description = models.CharField(max_length=200, null=False)
    coach = models.CharField(max_length=15, null=False)
    keywords = models.CharField(max_length=200, null=False)  # how to create a list
    capacity = models.PositiveIntegerField(null=False)
    current_capacity = models.PositiveIntegerField(default=0, editable=False)
    # recurrences = RecurrenceField(null=True)
    weekday = models.CharField(max_length=2, null=True)
    frequency2 = models.CharField(max_length=15, null=True)
    date_created = models.CharField(max_length=10, null=True)
    end_date = models.CharField(max_length=10, null=True)
    start_time = models.TimeField(null=False, default=datetime.datetime.now().strftime('%H:%M:%S'))
    end_time = models.TimeField(null=False)
    date = models.CharField(max_length=10, null=True)
    # end_date = models.DateField(null=False)
    # users = models.ManyToManyField(CustomUser, default=1)
    readonly_fields = ['current_capacity']

    def __str__(self):
        """Returns a string representation of the class"""
        return f'[{self.name}, {self.studio}, {self.id}, {self.date}]'

    def save(self, *args, **kwargs):
        """Saves the gym_class instance"""
        # super(GymClass, self).save(*args, **kwargs)
        super(GymClass, self).save(*args, **kwargs)
        gym_class = get_object_or_404(GymClass, pk=self.id)
        print(gym_class)
        # if request.data['current_capacity'] != 0:
        #     raise ValidationError('Cannot change this value')
        # if kwargs['date'] != None:
        #     raise ValidationError('Cannot change this value')

        # if kwargs['frequency2'] not in {'YEARLY', 'MONTHLY', 'WEEKLY', 'DAILY', 'HOURLY'}:
        # # raise ValueError('Please enter a valid frequency')
        #     raise ValidationError('Please enter a valid frequency')
        # if kwargs['weekday'] not in {'MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'}:
        #     raise ValidationError('Please enter a valid weekday')
        start = gym_class.date_created
        frequency = gym_class.frequency2
        freq2 = 0
        if frequency == 'YEARLY':
            freq2 = YEARLY
        if frequency == 'MONTHLY':
            freq2 = MONTHLY
        if frequency == 'WEEKLY':
            freq2 = WEEKLY
        if frequency == 'DAILY':
            freq2 = DAILY
        if frequency == 'HOURLY':
            freq2 = HOURLY

        weekday = gym_class.weekday
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

        date_format = '%Y-%m-%d'
        # try:
        #     datetime.datetime.strptime(start, date_format)
        # except ValueError:
        #     raise ValueError('Please enter a valid date')
        date_created = datetime.datetime.strptime(start, '%Y-%m-%d')
        end = gym_class.end_date
        # try:
        #     datetime.datetime.strptime(end, date_format)
        # except ValueError:
        #     raise ValidationError('Please enter a valid date')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
        count = abs(relativedelta(date_created, end_date).weeks) + 1  # number of recurring classes there should be

        dates = list(rrule(freq=freq2, byweekday=wday, dtstart=date_created, until=end_date))
        print(dates)
        created_classes = []
        id_start = gym_class.id + 1
        for i in range(1, len(dates)):  # the first instance already stores the first date in date
            date = dates[i].strftime('%Y-%m-%d')
            validated_data = {
                'id': id_start,
                'studio': gym_class.studio, 
                'name': gym_class.name, 
                'description': gym_class.description,
                'keywords': gym_class.keywords,
                'capacity': gym_class.capacity,
                # frequency=self.kwargs['frequency'], 
                'weekday': gym_class.weekday, 
                'date_created': gym_class.date_created,
                'start_time': gym_class.start_time,
                'end_time': gym_class.end_time,
                'end_date': gym_class.end_date,
                'date': date
            }
            # print(gym_class.studio.id)
            gym_class2 = gym_class
            gym_class2.create(validated_data)
            id_start += 1

            # gym_class2 = super(GymClass, gym_class).create(
            #     studio=gym_class.studio,
            #     name=gym_class.name,
            #     description=gym_class.description,
            #     keywords=gym_class.keywords,
            #     capacity=gym_class.capacity,
            #     # frequency=self.kwargs['frequency'], 
            #     weekday=gym_class.weekday, 
            #     date_created=gym_class.date_created,
            #     start_time=gym_class.start_time,
            #     end_time=gym_class.end_time,
            #     end_date=gym_class.end_date,
            #     date=dates[i]  
            # )
            # super(GymClass, gym_class2).save(*args, **kwargs)
            entry = {'name': gym_class2.name, 'studio': gym_class2.studio, 'id': gym_class2.id, 
                'date_created': dates[i]}
            created_classes.append(entry)
            
        return gym_class

    def create(self, validated_data):
        # print(validated_data['studio'])
        self.id = validated_data['id']
        self.studio=validated_data['studio']
        self.name=validated_data['name']
        self.description=validated_data['description']
        self.keywords=validated_data['keywords']
        self.capacity=validated_data['capacity']
        # frequency=self.kwargs['frequency'], 
        self.weekday=validated_data['weekday']
        self.date_created=validated_data['date_created']
        self.start_time=validated_data['start_time']
        self.end_time=validated_data['end_time']
        self.end_date=validated_data['end_date']
        self.date=validated_data['date']
        super(GymClass, self).save(validated_data)


    def delete(self, *args, **kwargs):
        super(GymClass, self).delete(*args, **kwargs)
    
    def delete_all(self, *args, **kwargs):
        actions = ('delete_all')
        queryset = GymClass.objects.filter(name=self.name, studio=self.studio)
        for gym_class in queryset:
            gym_class.delete()
    delete_all.short_description = 'Delete all classes of a certain type'

    def decrease_capacity(self):
        """Decreases the capacity of the class by modifying its "current_capacity" attribute"""
        self.current_capacity += 1
        return self.current_capacity

    def increase_capacity(self):
        """Increases the capacity of the class by modifying its "current_capacity" attribute"""
        self.current_capacity -= 1
        return self.current_capacity


class UserAndClass(models.Model):
    """Model that represents user-class relationship (through enrolment)
        user: the user that is enrolled in "class"
        gym_class: the class that "user" is enrolled in
    """
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, default=1)
    gym_class = models.ForeignKey(GymClass, on_delete=CASCADE, default=1)

    def __str__(self):
        return f'[{self.user}, {self.gym_class}]'
