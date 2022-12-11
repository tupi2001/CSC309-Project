from django.shortcuts import render
import jwt
from django.contrib.auth import login, logout
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
from accounts.serializers import CreateUserSerializer


class CreateUserView(CreateAPIView):
    """Create a user view to allow creation of a new user"""
    permission_classes = [AllowAny, ]
    serializer_class = CreateUserSerializer


class EditProfileView(UpdateAPIView):
    """Allow user to update or edit their profile"""
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer

    def patch(self, request, *args, **kwargs):
        """Patch method to update data of a specific user"""
        user_object = self.get_object()
        data = request.data

        #  check if the user_object and the requested user are the same
        # update user object fields and save new user information, then return response
        if user_object == self.request.user:
            user_object.username = data.get('username', user_object.username)
            user_object.set_password(data.get('password', user_object.password))
            user_object.email = data.get('email', user_object.email)
            user_object.first_name = data.get('first_name', user_object.first_name)
            user_object.last_name = data.get('last_name', user_object.last_name)
            user_object.avatar = data.get('avatar', user_object.avatar)
            user_object.phone_number = data.get('phone_number', user_object.phone_number)

            user_object.save()
            serializer = CreateUserSerializer(user_object)
            return Response(serializer.data)

        # user is not authorized to access this user information
        return Response({'error': 'Unauthenticated'})

class UserViewSet(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreateUserSerializer

    def get_object(self):
        return self.request.user

    def get(self, arg):
        serializer = CreateUserSerializer(self.get_object())
        return Response(serializer.data)