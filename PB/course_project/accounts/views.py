from django.shortcuts import render
import jwt
from django.contrib.auth import login, logout
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from classes.models import UserAndClass


# Create your views here.
class UpdateProfile(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user_object = self.request.user.pk

        return get_object_or_404(CustomUser, id=user_object)


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

        return Response({'status': status.HTTP_200_OK, 'Token': token.key})


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'status': status.HTTP_200_OK, 'Token': token.key})


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        request.user.auth_token.delete()
        logout(request)
        return Response('Successfully logged out!')


class ClassesView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        response = {}
        classes = UserAndClass.objects.filter(users=self)
        for gym_class in classes:
            class_info = gym_class.__dict__
            # class_info.pop('users')
            response[class_info['name']] = class_info.pop('name')

        return JsonResponse(response)
