from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def get_absolute_url(self):
        return reverse_lazy('accounting:category-detail', kwargs={'pk': self.pk})
