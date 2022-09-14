from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=256, unique=True)
    username = models.CharField(max_length=128, blank=True)

    EMAIL_FIELD = "username"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
