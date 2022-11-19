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
from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
# from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer, UserSerializer2, GetUserSerializer
from accounts.serializers import CreateUserSerializer


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = CreateUserSerializer


class EditProfileView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer

    def patch(self, request, *args, **kwargs):
        user_object = self.get_object()
        data = request.data

        if user_object == self.request.user:
            user_object.username = data.get('username', user_object.username)
            user_object.set_password = data.get('password', user_object.password)
            user_object.email = data.get('email', user_object.email)
            user_object.first_name = data.get('first_name', user_object.first_name)
            user_object.last_name = data.get('last_name', user_object.last_name)
            user_object.avatar = data.get('avatar', user_object.avatar)
            user_object.phone_number = data.get('phone_number', user_object.phone_number)

            user_object.save()
            serializer = CreateUserSerializer(user_object)
            return Response(serializer.data)

        return Response({'error': 'Unauthenticated'})

# class UpdateProfile2(generics.UpdateAPIView):
#     queryset = CustomUser.objects.all()
#     permission_classes = [IsAuthenticated]
#     # authentication_classes = [SessionAuthentication]
#     serializer_class = UserSerializer2
#
#     def post(self, request, *args, **kwargs):
#         print(self.request.user.pk, request.data)
#         serializer = UserSerializer2(self.request.user.pk, data=request.data)
#         # print(serializer)
#         return Response({'status': status.HTTP_200_OK})
#
#
# # Create your views here.
# class UpdateProfile(generics.UpdateAPIView):
#     queryset = CustomUser.objects.all()
#     permission_classes = [IsAuthenticated]
#     # authentication_classes = [SessionAuthentication]
#     serializer_class = UserSerializer
#
#     # permission_classes = [IsAuthenticated]
#     # serializer_class = UserSerializer
#
#     def get_object(self):
#         user_object = self.request.user.pk  # primary key
#         return get_object_or_404(CustomUser, id=user_object)
#
#
# class GetProfile(generics.RetrieveAPIView):
#     queryset = CustomUser.objects.all()
#     permission_classes = [IsAuthenticated]
#     serializer_class = GetUserSerializer
#     # authentication_classes = [SessionAuthentication]
#
#     def get_object(self):
#         user_object = self.request.user.pk  # primary key
#         return get_object_or_404(CustomUser, id=user_object)
#
#
# class RegisterView(generics.CreateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = RegisterSerializer(data=request.data, context={'request': request})
#
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#             token, created = Token.objects.get_or_create(user=user)
#
#         return Response({'status': status.HTTP_200_OK, 'Token': token.key})
#
#
# class LoginView(GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'status': status.HTTP_200_OK, 'Token': token.key})
#
#
# class LogoutView(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         print(request)
#         request.user.auth_token.delete()
#         logout(request)
#         return Response('Successfully logged out!')
