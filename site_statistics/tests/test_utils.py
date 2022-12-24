import datetime

from django.test import TestCase

from accounting.models import ExpensesUnit, IncomeUnit, Category
from site_statistics.utils import get_month_name, calculate_money, get_category_stats


class UtilsTestCase(TestCase):
    def test_get_month_name(self):
        self.assertEqual(get_month_name(5), 'May')

    def test_calculate_money(self):
        IncomeUnit.objects.create(name='test', income='50', receive_date='2022-12-31')
        IncomeUnit.objects.create(name='test1', income='25.50', receive_date='2023-01-01')
        ExpensesUnit.objects.create(name='test', price='50', purchase_date='2022-12-31')
        ExpensesUnit.objects.create(name='test1', price='95.50', purchase_date='2023-01-01')

        self.assertEqual(calculate_money(datetime.date(2023, 1, 1)).get('income'), 25.50)
        self.assertEqual(calculate_money(datetime.date(2023, 1, 1)).get('expenses'), 95.50)
        self.assertEqual(calculate_money(datetime.date(2023, 1, 1)).get('total'), -70)
        self.assertEqual(calculate_money().get('income'), 75.50)
        self.assertEqual(calculate_money().get('expenses'), 145.50)
        self.assertEqual(calculate_money().get('total'), -70)

    def test_get_category_stats(self):
        cat = Category.objects.create(name='test')
        cat.income_unit.add(IncomeUnit.objects.create(name='test', income='50', receive_date='2022-12-31'))
        cat.income_unit.add(IncomeUnit.objects.create(name='test1', income='25.50', receive_date='2023-01-01'))
        cat.expenses_unit.add(ExpensesUnit.objects.create(name='test', price='50', purchase_date='2022-12-31'))
        cat.expenses_unit.add(ExpensesUnit.objects.create(name='test1', price='95.50', purchase_date='2023-01-01'))

        self.assertEqual(get_category_stats(datetime.date(2022, 12, 31))[0].income, 50)
        self.assertEqual(get_category_stats(datetime.date(2022, 12, 31))[0].expenses, 50)
        self.assertEqual(get_category_stats()[0].income, 75.50)
        self.assertEqual(get_category_stats()[0].expenses, 145.50)
