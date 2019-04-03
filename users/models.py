from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    pass

class User(AbstractUser):
    def __str__(self):
        return self.username