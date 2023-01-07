from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from accounts.models import User
from accounting.models import Category, ExpensesUnit, IncomeUnit
from accounting.views import ExpensesUnitCreateView, RelatedCategoryMixin, SingleObjectSearchMixin
from accounting.forms import ExpensesUnitForm


class RelatedCategoryMixinTestCase(TestCase):
    def setUp(self) -> None:
        self.rf = RequestFactory()
    
    def test_post_ajax(self):
        request = self.rf.post(
            reverse_lazy('accounting:expenses-unit-create'),
            {'name': 'category'},
            HTTP_X_Requested_With='XMLHttpRequest',
            )

        mixin = RelatedCategoryMixin()
        resp = mixin.post(request)
        
        self.assertJSONEqual(str(resp.content, encoding='utf8'), {'id': 1})


class SingleObjectSearchMixinTestCase(TestCase):
    def setUp(self) -> None:
        self.rf = RequestFactory()
    
    def test_get_queryset_request_data_empty(self):
        expected = [
            ExpensesUnit.objects.create(
                name=f'expenses{i}',
                quantity=1,
                price=2,
                purchase_date='2023-01-04',
                ) for i in range(2)
            ]

        mixin = SingleObjectSearchMixin()
        mixin.model = ExpensesUnit

        mixin.filters = {
            'name': 'name__icontains',
            'quantity': 'quantity',
            'created': 'created__date',
            'categories': 'categories__name__in',
            'total_price': 'total_price',
            'total_income': 'total_income',
            'purchase_date': 'purchase_date',
            'receive_date': 'receive_date',
            }
        
        mixin.ordering = '-created'

        mixin.request = self.rf.get(reverse_lazy('accounting:unit-list'))
        queryset = mixin.get_queryset()
        queryset = [queryset[i] for i in range(len(queryset))]
 
        self.assertEqual(queryset, expected)

    def test_get_queryset_key_model(self):
        expected = [
            ExpensesUnit.objects.create(
                name='expenses',
                quantity=1,
                price=2,
                purchase_date='2023-01-04',
                ),
            ]
        
        IncomeUnit.objects.create(
                name='income',
                quantity=1,
                income=2,
                receive_date='2023-01-04',
                )
        
        mixin = SingleObjectSearchMixin()
        mixin.model_dict = {'expenses': ExpensesUnit, 'income': IncomeUnit}

        mixin.filters = {
            'name': 'name__icontains',
            'quantity': 'quantity',
            'created': 'created__date',
            'categories': 'categories__name__in',
            'total_price': 'total_price',
            'total_income': 'total_income',
            'purchase_date': 'purchase_date',
            'receive_date': 'receive_date',
            }
        
        mixin.ordering = '-created'

        mixin.request = self.rf.get(
            reverse_lazy('accounting:unit-list'),
            {'model': 'expenses'},
            )
        
        queryset = mixin.get_queryset()
        queryset = [queryset[i] for i in range(len(queryset))]

        self.assertEqual(queryset, expected)

    def test_get_queryset_key_order_by(self):
        expected = [
            ExpensesUnit.objects.create(
                name=f'{i}expenses',
                quantity=1,
                price=2,
                purchase_date='2023-01-04',
                ) for i in range(2)
            ]
        
        mixin = SingleObjectSearchMixin()
        mixin.model = ExpensesUnit

        mixin.filters = {
            'name': 'name__icontains',
            'quantity': 'quantity',
            'created': 'created__date',
            'categories': 'categories__name__in',
            'total_price': 'total_price',
            'total_income': 'total_income',
            'purchase_date': 'purchase_date',
            'receive_date': 'receive_date',
            }
        
        mixin.ordering = '-created'

        mixin.request = self.rf.get(
            reverse_lazy('accounting:unit-list'),
            {'order_by': 'name'},
            )
        
        queryset = mixin.get_queryset()
        queryset = [queryset[i] for i in range(len(queryset))]

        self.assertEqual(queryset, expected)

    def test_get_queryset_key_in(self):
        expected = [
            ExpensesUnit.objects.create(
                name='expenses0',
                quantity=1,
                price=2,
                purchase_date='2023-01-04',
                )
            ]
        
        ExpensesUnit.objects.create(
                name='expenses1',
                quantity=1,
                price=2,
                purchase_date='2023-01-04',
                )
        
        Category.objects.create(name='cat').expenses_unit.add(expected[0])

        mixin = SingleObjectSearchMixin()
        mixin.model = ExpensesUnit

        mixin.filters = {
            'name': 'name__icontains',
            'quantity': 'quantity',
            'created': 'created__date',
            'categories': 'categories__name__in',
            'total_price': 'total_price',
            'total_income': 'total_income',
            'purchase_date': 'purchase_date',
            'receive_date': 'receive_date',
            }
        
        mixin.ordering = 'name'

        mixin.request = self.rf.get(
            reverse_lazy('accounting:unit-list'),
            {'categories': 'cat'},
            )
        
        queryset = mixin.get_queryset()
        queryset = [queryset[i] for i in range(len(queryset))]

        self.assertEqual(queryset, expected)
    
    def test_get_queryset_other_keys(self):
        expected = [
            ExpensesUnit.objects.create(
                name='expenses0',
                quantity=1,
                price=2,
                purchase_date='2023-01-04',
                )
            ]
        
        ExpensesUnit.objects.create(
                name='expenses1',
                quantity=1,
                price=2,
                purchase_date='2023-01-04',
                )

        mixin = SingleObjectSearchMixin()
        mixin.model = ExpensesUnit

        mixin.filters = {
            'name': 'name__icontains',
            'quantity': 'quantity',
            'created': 'created__date',
            'categories': 'categories__name__in',
            'total_price': 'total_price',
            'total_income': 'total_income',
            'purchase_date': 'purchase_date',
            'receive_date': 'receive_date',
            }
        
        mixin.ordering = '-created'

        mixin.request = self.rf.get(
            reverse_lazy('accounting:unit-list'),
            {'name': 'expenses0'},
            )
        
        queryset = mixin.get_queryset()
        queryset = [queryset[i] for i in range(len(queryset))]

        self.assertEqual(queryset, expected)
