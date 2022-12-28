from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy

from accounts.models import User
from accounting.models import Category, ExpensesUnit, IncomeUnit
from accounting.views import ExpensesUnitCreateView
from accounting.forms import ExpensesUnitForm


class ExpensesUnitCreateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(email='test@email.com', username='test', password='test')

    def test_response_code_is_200(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('accounting:expenses-unit-create'))

        self.assertEqual(resp.status_code, 200)

    def test_template_used(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('accounting:expenses-unit-create'))

        self.assertTemplateUsed(resp, 'accounting/unit_create.html')

    def test_post_ajax(self):
        self.client.force_login(self.user)

        resp = self.client.post(
            reverse_lazy('accounting:expenses-unit-create'),
            {'name': 'test'},
            HTTP_X_Requested_With='XMLHttpRequest',
            )

        cat = Category.objects.get(id=1)

        self.assertJSONEqual(str(resp.content, encoding='utf-8'), {'id': cat.id})

    def test_form_valid_with_categories(self):
        form = ExpensesUnitForm({'name': 'test', 'quantity': 1, 'price': 100, 'purchase_date': '2022-12-27'})
        cat = Category.objects.create(name='test')
        view = ExpensesUnitCreateView(categories=[cat])
        view.categories
        view.form_valid(form)
        
        e = ExpensesUnit.objects.get(id=1)
        print(e.categories.all())
