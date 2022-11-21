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

class CreateClassView(CreateAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]

    queryset = GymClass.objects.all()
    serializer_class = ClassSerializer

    def post(self, request):
        print("hello")
        serializer = ClassSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            gym_class = serializer.save()
            print(gym_class)
        # print(hello)
        return Response({'status': status.HTTP_200_OK})


class UpdateClassView(UpdateAPIView):
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
    def post(self, request, *args, **kwargs):
        return get_object_or_404(GymClass, pk=self.kwargs['class_id'])


class DeleteClassView(DestroyAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    queryset = GymClass.objects.all()
    serializer_class = ClassSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(GymClass, pk=self.kwargs['class_id'])
        instance.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT})


class DeleteClassesView(DestroyAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = ClassSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        gym_class = get_object_or_404(GymClass, pk=self.kwargs['class_id'])
        queryset = GymClass.objects.filter(name=gym_class.name, studio=gym_class.studio)
        for gym_class in queryset:
            gym_class.delete()

        return Response({'status': status.HTTP_204_NO_CONTENT})


# class ClassView(RetrieveAPIView):
#     serializer_class = ClassSerializer

#     def get_object(self):
#         return get_object_or_404(Class, id=self.kwargs['product_id'])


class ClassesView(ListAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [AllowAny]
    serializer_class = ClassSerializer

    def get(self, request, *args, **kwargs):
        today = now().time()
        studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
        set = GymClass.objects.filter(studio=self.kwargs['studio_id'])
        set2 = set.filter(start_time__gte=today).order_by('start_time')
        print(set)
        # response = []
        # for gym_class in set2:
        #     class_info = gym_class.__dict__
        #     # print(gy)
        #     # response[gym_class.name] = [ {gym_class.studio.__dict__}, gym_class.id]
        #     response.append(list())

        classes = []

        for gym_class in set2:
            dict = {
                'name':gym_class.name,
                'class_id': gym_class.id,
                'start_time': gym_class.start_time
            }
            classes.append(dict)

        data = {'gym_class': classes}

        return Response(data)


class EnrolUserInClassView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    queryset = UserAndClass.objects.all()
    serializer_class = UserAndClassSerializer

    def post(self, request, *args, **kwargs):
        gym_class = get_object_or_404(GymClass, pk=self.kwargs['class_id'])
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        # serializer = UserAndClassSerializer(data=request.data, context={'request': request})
        if not UserAndClass.objects.filter(gym_class=gym_class, user=user).exists():
            if gym_class.current_capacity < gym_class.capacity:
                userandclass = UserAndClass.objects.create(
                    gym_class=gym_class,
                    user=user
                )
                gym_class.current_capacity += 1
                userandclass.save()
        
        return Response({'status': status.HTTP_200_OK})


class EnrolUserInClassesView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    queryset = UserAndClass.objects.all()
    serializer_class = UserAndClassSerializer

    def post(self, request, *args, **kwargs):
        gym_class = get_object_or_404(GymClass, pk=self.kwargs['class_id'])
        user = get_object_or_404(CustomUser, pk=self.request.user.id)
        all_gym_classes = GymClass.objects.filter(studio=gym_class.studio, name=gym_class.name)
        # serializer = UserAndClassSerializer(data=request.data, context={'request': request})
        for gym_class in all_gym_classes:
            if not UserAndClass.objects.filter(gym_class=gym_class, user=user).exists():
                if gym_class.current_capacity < gym_class.capacity:
                    userandclass = UserAndClass.objects.create(
                        gym_class=gym_class,
                        user=user
                    )
                    gym_class.current_capacity += 1
                    userandclass.save()
        
        return Response({'status': status.HTTP_200_OK})      


class RemoveUserFromClassView(DestroyAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    queryset = UserAndClass.objects.all()
    serializer_class = UserAndClassSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        gym_class = get_object_or_404(GymClass, pk=self.kwargs['class_id'])
        instance = get_object_or_404(UserAndClass, gym_class=self.kwargs['class_id'], 
                user=self.request.user)
        print(instance)
        instance.delete()
        # get_object_or_404(UserAndClass, gym_class=self.kwargs['class_id'], 
        #         user=self.request.user)
        gym_class.current_capacity -= 1
        gym_class.save()
        return Response(status=request.status.HTTP_204_NO_CONTENT)


class RemoveUserFromClassesView(DestroyAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = UserAndClassSerializer
    # lookup_field = 'id'

    def get(self, request, name=None, studio=None):
        queryset = UserAndClass.objects.filter(name=name, studio=self.kwargs['studio_id'], 
                user=self.request.user.id)  # change
        # queryset2 = queryset.filter()
        for gym_class in queryset:
            gym_class.delete()

        return Response(status=request.status.HTTP_204_NO_CONTENT)


class UserClassesView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response = {}
        gym_classes = UserAndClass.objects.filter(user=self.request.user.id)
        # gym_class = GymClass.objects.filter(name=gym_classes.gym_class.name)
        # print(self.request.user)
        # for gym_class in classes:
        #     class_info = gym_class.__dict__
        #     # class_info.pop('users')
        #     response[class_info['name']] = class_info.pop('name')

        # for gym_class in classes:
        #     class_info = gym_class.__dict__
        #     # print(gy)
        #     # response[gym_class.name] = [ {gym_class.studio.__dict__}, gym_class.id]
        #     response.append(list())

        classes = []

        for gym_class in gym_classes:
            
            dict = {
                'username':gym_class.user.username,
                'class_name': gym_class.gym_class.name,
                'id': gym_class.gym_class.id
            }
            classes.append(dict)

        data = {'gym_class': classes}
        print(data)
        return Response(data)