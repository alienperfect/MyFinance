from django.test import TestCase

from site_statistics.forms import StatisticsForm


class StatisticsFormTestCase(TestCase):
    def test_field_labels(self):
        form = StatisticsForm()
        self.assertEqual(form.fields['month_year'].label , 'Month')
