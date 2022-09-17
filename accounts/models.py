from django.db import models
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)


class User(AbstractUser):
    email = models.EmailField(max_length=256, unique=True)
    username = models.CharField(max_length=128, blank=True)

    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    job_position = models.CharField(max_length=256, blank=True)
    monthly_salary = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    hours_worked = models.PositiveIntegerField(blank=True, null=True)
    total_earned = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    EMAIL_FIELD = "username"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
