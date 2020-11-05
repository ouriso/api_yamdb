from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        pass

    def create_superuser(self, email, date_of_birth, password=None):
        pass


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, "user"),
        (2, "moderator"),
        (3, "admin"),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    bio = models.TextField(max_length=500, blank=True)
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    objects = UserManager()