from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property

from accounts.utils import user_directory_path


class User(AbstractUser):
    email = models.EmailField(max_length=256, unique=True)
    username = models.CharField(max_length=128, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    job_position = models.CharField(max_length=64, blank=True)

    EMAIL_FIELD = "username"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Account(models.Model):
    monthly_salary = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    hours_worked = models.PositiveIntegerField(blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @cached_property
    def calculate_total(self):
        total = 0
        if self.hourly_rate and self.hours_worked:
            total = self.hourly_rate * self.hours_worked
        elif self.monthly_salary:
            total = self.monthly_salary
        return total
