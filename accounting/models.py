from django.db import models
from django.utils.functional import cached_property

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
    quantity = models.PositiveIntegerField(default=1)
    objects = AccountingUnitManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ExpensesUnit(AccountingUnit):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    purchase_date = models.DateField()
    categories = models.ManyToManyField('Category', related_name='expenses_unit', blank=True)

    @cached_property
    def calculate_total_price(self):
        return self.quantity * self.price

    def save(self, **kwargs):
        self.total_price = self.calculate_total_price
        return super().save(**kwargs)


class IncomeUnit(AccountingUnit):
    income = models.DecimalField(max_digits=8, decimal_places=2)
    total_income = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    receive_date = models.DateField()
    categories = models.ManyToManyField('Category', related_name='income_unit', blank=True)

    @cached_property
    def calculate_total_income(self):
        return self.quantity * self.income

    def save(self, **kwargs):
        self.total_income = self.calculate_total_income
        return super().save(**kwargs)
