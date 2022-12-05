import datetime
import calendar

from django.db.models import Sum, Q

from accounting.models import ExpensesUnit, IncomeUnit, Category


def get_month_name(month: int) -> str:
    """Get month name."""
    return calendar.month_name[month]


def calculate_money(date: datetime.date = None) -> dict:
    """Calculate income and expenses."""
    money_dict = {}

    if date:
        income = IncomeUnit.objects.filter(
            receive_date__month=date.month, receive_date__year=date.year,
            ).aggregate(income=Sum('income')).get('income')

        expenses = ExpensesUnit.objects.filter(
            purchase_date__month=date.month, purchase_date__year=date.year,
            ).aggregate(price=Sum('price')).get('price')
    else:
        income = IncomeUnit.objects.aggregate(income=Sum('income')).get('income')
        expenses = ExpensesUnit.objects.aggregate(price=Sum('price')).get('price')

    money_dict['income'] = round(income, 2) if income else income
    money_dict['expenses'] = round(expenses, 2) if expenses else expenses

    if income and expenses:
        money_dict['total'] = round(income - expenses, 2)

    return money_dict


def get_category_stats(date: datetime.date = None) -> dict:
    """Get category stats."""
    category_stats = []
 
    if date:
        category_stats.append(
            Category.objects.filter(
                Q(income_unit__receive_date__month=date.month, income_unit__receive_date__year=date.year)
                | Q(expenses_unit__purchase_date__month=date.month, expenses_unit__purchase_date__year=date.year)
                ).annotate(income=Sum('income_unit__income'), expenses=Sum('expenses_unit__price'))
            )
    else:
        category_stats.append(
            Category.objects.annotate(income=Sum('income_unit__income'), expenses=Sum('expenses_unit__price'))
        )

    return category_stats
