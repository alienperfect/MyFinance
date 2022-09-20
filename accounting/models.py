from django.db import models


class AccountingUnit(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
