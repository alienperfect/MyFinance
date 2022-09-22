from django.contrib import admin

from accounting.models import AccountingUnit, Category

admin.site.register(AccountingUnit)
admin.site.register(Category)
