from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
# from classes.models import UserAndClass


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email or not username:
            raise ValueError('This is a required field')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    password2 = models.CharField(max_length=100, blank=True, null=True)
    # phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    phone_number = models.CharField(max_length=15)
    avatar = models.ImageField(null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = AccountManager()

    class Meta:
        db_table = 'users_table'

    def __str__(self):
        return str(self.username)

    def has_permission(self, permission, object=None):
        return self.is_superuser

    def module_permission(self, app_label):
        return self.is_superuser
