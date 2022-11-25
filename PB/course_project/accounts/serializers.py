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


class CreateUserSerializer(serializers.ModelSerializer):
    """Creating the user"""
    # password errors and styles , hidden password value
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={'min_length': f"Password too short!"},
        style={'input_type': 'password'}
    )

    # password errors and styles , hidden password value
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={'min_length': f"Password too short!"},
        style={'input_type': 'password'}
    )

    class Meta:
        """Fields of a user
            Parameters:
                pk: primary key
                first_name: first name
                last_name : last name
                username: username of a user
                email: email of a user
                password: password of a user
                password2: repeated password of a user, constraint: password == password2
                phone_number: phone number of a user
                avatar: user's avatar must be an image
        """
        model = CustomUser
        fields = ['pk', 'first_name', 'last_name', 'username', 'email', 'password', 'password2',
                  'phone_number', 'avatar'
                  ]

    def validate_username(self, data):
        """Make sure the username follows specific constraints"""
        username = data

        # username cannot be less than 4 characters
        if len(username) < 4:
            raise serializers.ValidationError("Username must contain at least 4 characters")

        # check if user exists
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists")

        return username

    def validate_email(self, data):
        "Check that the email of the user is fine"
        email = data

        # check if email is empty
        if email != '':
            validator = EmailValidator(message='Email invalid')
            # validate email using validator
            validator(email)

        return email

    def validate_phone_number(self, data):
        """check that the phone number is valid"""
        phone_number = data
        # check that the phone number follows the format: (444)-444-4444, might change for usability
        phone_regex = re.compile('^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')

        # check that is follows the regx
        if not phone_regex.match(phone_number):
            raise serializers.ValidationError('Phone number invalid')

    #     return phone_number

    def validate(self, validated_data):
        """Validate password"""
        password = validated_data['password']
        password2 = validated_data['password2']

        # make sure password is not empty
        if password != '':
            # make sure length of password is at least 8
            if len(password) < 8:
                raise serializers.ValidationError(
                    'Password too short. Must be at least 8 characters')
        # make sure the two passwords match
        if password != password2:
            raise serializers.ValidationError("Two passwords don't match")

        return validated_data

    def create(self, validated_data):
        """Create the new user using the data validated"""
        user = CustomUser.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            avatar=validated_data['avatar'],
            username=validated_data['username'],
            email=validated_data['email']
        )

        # set the password and save the user
        user.set_password(validated_data['password'])
        user.save()
        return user
