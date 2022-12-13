from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from classes.models import GymClass, UserAndClass
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from classes.serializers import ClassSerializer, UserAndClassSerializer
from django.utils.timezone import now
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from studios.models import Studio
from accounts.models import CustomUser
from django.db.models import Q
from datetime import datetime, timedelta

class CreateClassView(CreateAPIView):
    """Creates a class for a studio"""
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]

    queryset = GymClass.objects.all()
    serializer_class = ClassSerializer

    def post(self, request):
        """Creates a class from user input"""
        serializer = ClassSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            gym_class = serializer.save()
        return Response({'status': status.HTTP_200_OK, 'class_id': gym_class.id})


class UpdateClassView(UpdateAPIView):
    """Updates a class in a particular studio"""
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    queryset = GymClass.objects.all()
    serializer_class = ClassSerializer
    lookup_field = 'id'
  
    # def get_object(self, request, *args, **kwargs):
    #     instance = get_object_or_404(Class, pk=self.kwargs['class_id'])
    #     serializer = ClassSerializer(instance, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()

    #     return Response(serializer.data)
    def post(self, request, *args, **kwargs): # change this
        return get_object_or_404(GymClass, pk=self.kwargs['class_id'])


class DeleteClassView(DestroyAPIView):
    """Deletes a class that belongs to a specific studio"""
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    queryset = GymClass.objects.all()
    serializer_class = ClassSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        """Gets studio id and class id to delete the proper class"""
        studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
        instance = get_object_or_404(GymClass, pk=self.kwargs['class_id'], studio=studio)
        instance.delete()
        return Response({'status': 'class was deleted successfully'})


class DeleteClassesView(DestroyAPIView):
    """Deletes classes of a certain type that belongs to a specific studio"""
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = ClassSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        """Gets studio id and class id to delete the proper classes"""
        studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
        gym_class = get_object_or_404(GymClass, pk=self.kwargs['class_id'], studio=studio)
        queryset = GymClass.objects.filter(name=gym_class.name, studio=gym_class.studio)
        for gym_class in queryset:
            gym_class.delete()

        return Response({'status': 'classes were deleted successfully'})


class ClassesView(ListAPIView):
    """List the classes that belong to a certain studio"""
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = ClassSerializer

    def get(self, request, *args, **kwargs):
        """Gets studio id to list all classes that belong to that studio"""
        today = now().time()
        studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
        print(studio.name)
        set = GymClass.objects.filter(studio=self.kwargs['studio_id'])
        # print(set)
        # for gym_class in set:
        #     print(type(gym_class.date) == datetime)
        #     gym_class.date = datetime.strptime(gym_class.date, '%Y-%m-%d')
            # except:
            #     gym_class.date = datetime.strptime(gym_class.date, '%m/%d/%Y')
        print(set)
        # str_date = gym_class.date.now.strftime("%m/%d/%Y
        # set2 = set.filter(date__gte = datetime.now()).order_by('start_time')
        # start_date = datetime.datetime.strptime(date, '%m/%d/%Y')
        set2 = set.filter(date__gte = datetime.now()-timedelta(days=1)).order_by('date')

        classes = []

        for gym_class in set2:
            dict = {
                'name':gym_class.name,
                'class_id': gym_class.id,
                'start_time': gym_class.start_time,
                'start_date': gym_class.date
            }
            classes.append(dict)

        data = {'gym_classes': classes}

        return Response(data)


class EnrolUserInClassView(CreateAPIView):
    """Enrol user in a class in one studio"""
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    queryset = UserAndClass.objects.all()
    serializer_class = UserAndClassSerializer

    def get(self, request, *args, **kwargs):
        """Get studio id and class id to enrol user in specific class"""
        studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
        gym_class = get_object_or_404(GymClass, pk=self.kwargs['class_id'], studio=studio)
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        # serializer = UserAndClassSerializer(data=request.data, context={'request': request})
        if not UserAndClass.objects.filter(gym_class=gym_class, user=user).exists():
            if user.user_is_active():
                if gym_class.current_capacity < gym_class.capacity:
                    userandclass = UserAndClass.objects.create(
                        gym_class=gym_class,
                        user=user
                    )
                    gym_class.increase_capacity()
                    userandclass.save()
                else:
                    return Response({'status': 'capacity full, cannot enrol'})
            else:
                return Response({'status': 'user doesn\'t have an active subscription, cannot enrol'})
        
        return Response({'status': 'user was successfully enrolled'})


class EnrolUserInClassesView(CreateAPIView):
    """Enrol user in a class in a specific studio"""
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    queryset = UserAndClass.objects.all()
    serializer_class = UserAndClassSerializer

    def get(self, request, *args, **kwargs):
        """Get studio id and class id to enrol user in a specific type of class"""
        studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
        gym_class = get_object_or_404(GymClass, pk=self.kwargs['class_id'], studio=studio)
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        all_gym_classes = GymClass.objects.filter(studio=gym_class.studio, name=gym_class.name, 
                start_time=gym_class.start_time)
        # serializer = UserAndClassSerializer(data=request.data, context={'request': request})
        for gym_class in all_gym_classes:
            capacity = True
            if not UserAndClass.objects.filter(gym_class=gym_class, user=user).exists():
                if user.user_is_active():
                    if gym_class.current_capacity < gym_class.capacity:
                        userandclass = UserAndClass.objects.create(
                            gym_class=gym_class,
                            user=user
                        )
                        gym_class.increase_capacity()
                        userandclass.save()
                else:
                    return Response({'status': 'user doesn\'t have an active subscription, cannot enrol'})
            else:
                capacity = False
        if not capacity:
            return Response({'status': 'capacity full in at least one class'})
        
        return Response({'status': 'user was successfully enrolled in all classes'})    


class RemoveUserFromClassView(DestroyAPIView):
    """Remove user from a class in a specific studio"""
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = UserAndClass.objects.all()
    serializer_class = UserAndClassSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        """Get studio id and class id to remove user from specific class"""
        studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
        gym_class = get_object_or_404(GymClass, pk=self.kwargs['class_id'], studio=studio)
        instance = get_object_or_404(UserAndClass, gym_class=self.kwargs['class_id'], 
                user=self.request.user)
        print(instance)
        instance.delete()
        # get_object_or_404(UserAndClass, gym_class=self.kwargs['class_id'], 
        #         user=self.request.user)
        gym_class.decrease_capacity()
        gym_class.save()
        return Response({'status': 'successfully enrolled in classes'}) 


class RemoveUserFromClassesView(DestroyAPIView):
    """Remove user from a type of class in a specific studio"""
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = UserAndClassSerializer
    # lookup_field = 'id'

    def get(self, request, name=None, studio=None):
        """Get studio id and class id to remove user from a specific type of class"""
        studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
        queryset = UserAndClass.objects.filter(name=name, studio=studio, 
                user=self.request.user.id, start_time=gym_class.start_time)  # change
        # queryset2 = queryset.filter()
        for gym_class in queryset:
            gym_class.gym_class.decrease_capacity()
            gym_class.delete()

        return Response({'status': 'successfully unenrolled in classes'}) 


class UserClassesView(ListAPIView):
    """List user's class schedule"""
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """Get user id to list all classes that the user is enrolled in"""
        response = {}
        gym_classes = UserAndClass.objects.filter(user=self.request.user.id)

        classes = []

        for gym_class in gym_classes:
            
            dict = {
                'username':gym_class.user.username,
                'class_name': gym_class.gym_class.name,
                'id': gym_class.gym_class.id,
                'start_date': gym_class.gym_class.date,
                'start_time': gym_class.gym_class.start_time, 
                'end_time': gym_class.gym_class.end_time
            }
            classes.append(dict)

        return JsonResponse(classes, safe=False)