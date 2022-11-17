from django.shortcuts import render
import jwt
from django.contrib.auth import login, logout
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
from accounts.serializers import LoginSerializer, RegisterSerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception = True):
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)

        return Response({'status': status.HTTP_200_OK, 'Token': token.key})


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data = request.data, context = {'request': request})

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
        return Response('Successfully logged in!')