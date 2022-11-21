import re
from django.contrib.auth import authenticate
from django.db import models
from django.core.validators import EmailValidator
from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

class UserSerializer(serializers.ModelSerializer):
    model = CustomUser
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar', 'phone_number']
        read_only_field = ['password', 'password2']


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar', 'phone_number',
                  'password', 'password2']

    def validate_username(self, data):
        username = data

        if len(username) < 4:
            raise serializers.ValidationError("Username must contain at least 4 characters")

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")

        return username

    def validate_email(self, data):
        email = data

        if email != '':
            validator = EmailValidator(message='Email invalid')
            validator(email)

        return email

    # def validate_phone_number(self, data):
    #     phone_number = data
    #     phone_regex = re.compile('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')

    #     if not phone_regex.match(phone_number):
    #         raise serializers.ValidationError('Phone number invalid')

    #     return phone_number

    def validate(self, validated_data):
        password = validated_data['password']
        password2 = validated_data['password2']

        if password != '':

            if len(password) < 8:
                raise serializers.ValidationError(
                    'Password too short. Must be at least 8 characters')

        if password != password2:
            raise serializers.ValidationError("Two passwords don't match")

        return validated_data

    def create(self, data):
        if 'avatar' in data:
            avatar = data["avatar"]
        else:
            avatar = None

        user = CustomUser.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            avatar=avatar,
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            raise serializers.ValidationError("Username is required")
        if not password:
            raise serializers.ValidationError("Password is required")

        user = CustomUser.objects.filter(username=username)
        if user.exists() and user.count() == 1:
            user_object = user.first()
        else:
            raise serializers.ValidationError(
                "Username or Email is invalid.")

        if user_object:
            if not user_object.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        data['user'] = user_object
        return data
