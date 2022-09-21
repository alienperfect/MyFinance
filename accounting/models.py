from django.db import models

from django_extensions.db.models import TimeStampedModel


class AccountingUnit(TimeStampedModel, models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateField()
    category = models.ManyToManyField('Category', related_name='accounting_unit', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
