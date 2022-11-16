from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from classes.models import Class
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from classes.serializers import ClassSerializer


class CreateClassView(CreateAPIView):
    permission_classes = [IsAdminUser]

    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def create(self, request):
        serializer = serializer.ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': request.status.HTTP_200_OK})
        else:
            return Response(serializer.errors, status=request.status.HTTP_400_BAD_REQUEST)


class UpdateClassView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    lookup_field = 'id'

    def update(self, request):
        instance = self.get_object()
        serializer = serializer.ClassSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class DeleteClassView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    lookup_field = 'id'

    def delete(self, request):
        instance = self.get_object
        instance.delete()
        return Response(status=request.status.HTTP_204_NO_CONTENT)


class DeleteClassesView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ClassSerializer
    # lookup_field = 'id'

    def delete(self, request, name=None, studio=None):
        queryset = Class.objects.filter(name=name)
        queryset2 = queryset.filter(studio=studio)
        for gym_class in queryset2:
            gym_class.delete()

        return Response(status=request.status.HTTP_204_NO_CONTENT)


# class ClassView(RetrieveAPIView):
#     serializer_class = ClassSerializer

#     def get_object(self):
#         return get_object_or_404(Class, id=self.kwargs['product_id'])


class ClassesView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassSerializer

    def get_queryset(self, studio=None):
        return Class.objects.filter(studio=studio)