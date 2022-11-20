from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
# from classes.models import UserAndClass


class AccountManager(BaseUserManager):
    """BaseUser model"""
    def create_user(self, email, username, password):
        """Check the email and username"""
        if not email or not username:
            raise ValueError('This is a required field')

        # create user using email and username
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        # set password to database
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """create superuser"""
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
    """Model that holds the attributes for a user
        Parameters:
            first_name: first name
            last_name : last name
            username: username of a user
            email: email of a user
            password: password of a user
            password2: repeated password of a user, constraint: password == password2
            phone_number: phone number of a user
            avatar: user's avatar must be an image
    """
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    password2 = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    avatar = models.ImageField(null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = AccountManager()

    class Meta:
        """database"""
        db_table = 'users_table'

    def __str__(self):
        """returns username as a string"""
        return str(self.username)

    def has_permission(self, permission, object=None):
        """Returns whether the user has permission"""
        return self.is_superuser

    def module_permission(self, app_label):
        """returns module permission"""
        return self.is_superuser
