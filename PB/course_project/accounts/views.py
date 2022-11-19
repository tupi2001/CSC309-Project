from django.shortcuts import render
import jwt
from django.contrib.auth import login, logout
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
<<<<<<< HEAD
=======
from django.http import JsonResponse
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
<<<<<<< HEAD
from accounts.serializers import LoginSerializer, RegisterSerializer


# Create your views here.
=======
from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer


# Create your views here.
class UpdateProfile(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        user_object = self.request.user.pk

        return get_object_or_404(CustomUser, id=user_object)

>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18

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
<<<<<<< HEAD

=======
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
<<<<<<< HEAD

=======
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
        return Response({'status': status.HTTP_200_OK, 'Token': token.key})


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        request.user.auth_token.delete()
        logout(request)
<<<<<<< HEAD
        return Response('Successfully logged in!')
=======
        return Response('Successfully logged out!')
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
