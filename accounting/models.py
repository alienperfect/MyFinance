from django.db import models

from django_extensions.db.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class AccountingUnitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('categories')


class AccountingUnit(TimeStampedModel):
    name = models.CharField(max_length=64)
    objects = AccountingUnitManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ExpensesUnit(AccountingUnit):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateField()
    categories = models.ManyToManyField('Category', related_name='expenses_unit', blank=True)


class IncomeUnit(AccountingUnit):
    income = models.DecimalField(max_digits=8, decimal_places=2)
    receive_date = models.DateField()
    categories = models.ManyToManyField('Category', related_name='income_unit', blank=True)
