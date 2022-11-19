import datetime
import calendar

from django.db.models import Sum

from accounting.models import ExpensesUnit, IncomeUnit, Category


def get_month_name(month: int) -> str:
    return calendar.month_name[month]


def calculate_money(date: datetime.date) -> dict:
    """Calculate income and expenses."""
    money_dict = {}

    if date:
        income = IncomeUnit.objects.filter(
            receive_date__month=date.month, receive_date__year=date.year,
            ).aggregate(Sum('income')).get('income__sum')

        expenses = ExpensesUnit.objects.filter(
            purchase_date__month=date.month, purchase_date__year=date.year,
            ).aggregate(Sum('price')).get('price__sum')
    else:
        income = IncomeUnit.objects.aggregate(Sum('income')).get('income__sum')
        expenses = ExpensesUnit.objects.aggregate(Sum('price')).get('price__sum')
        
    money_dict['income'] = round(income, 2) if income else income
    money_dict['expenses'] = round(expenses, 2) if expenses else expenses

    if income and expenses:
        money_dict['total'] = round(income - expenses, 2)

    return money_dict


def get_category_stats(date: datetime.date) -> dict:
    cat_stats = {}
    categories = Category.objects.all().prefetch_related('income_unit', 'expenses_unit')

    if date:
        for category in categories:
            income = category.income_unit.filter(
                receive_date__month=date.month, receive_date__year=date.year,
                ).aggregate(Sum('income')).get('income__sum')

            expenses = category.expenses_unit.filter(
                purchase_date__month=date.month, purchase_date__year=date.year,
                ).aggregate(Sum('price')).get('price__sum')

            cat_stats[category.name] = [
                round(income, 2) if income else None,
                round(expenses, 2) if expenses else None,
                ]
    else:
        for category in categories:
            income = category.income_unit.all().aggregate(Sum('income')).get('income__sum')
            expenses = category.expenses_unit.all().aggregate(Sum('price')).get('price__sum')

            cat_stats[category.name] = [
                round(income, 2) if income else None,
                round(expenses, 2) if expenses else None,
                ]

    print(cat_stats)
    return cat_stats
