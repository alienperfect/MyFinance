from django.db import models

from django_extensions.db.models import TimeStampedModel


class AccountingUnitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('categories')


class AccountingUnit(TimeStampedModel):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateField()
    categories = models.ManyToManyField('Category', related_name='accounting_unit', blank=True)
    objects = AccountingUnitManager()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
