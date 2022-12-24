from django.test import TestCase, Client
from django.urls import reverse_lazy

from accounts.models import User
from site_statistics.forms import StatisticsForm


class StatisticsViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.client = Client()
        cls.user = User.objects.create_user(email='test@email.com', username='test', password='test')

    def test_response_code_is_200(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('statistics:main'))

        self.assertEqual(resp.status_code, 200)

    def test_kwargs(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('statistics:main'), {'month_year': '09/2022'})
        
        self.assertIn('month_year', resp.context)
        self.assertEqual(type(resp.context.get('form', '')), type(StatisticsForm()))
        self.assertIn('money_dict', resp.context)
        self.assertIn('category_stats', resp.context)

    def test_template_used(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('statistics:main'))

        self.assertTemplateUsed(resp, 'site_statistics/main.html')
