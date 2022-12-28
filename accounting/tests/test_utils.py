from django.test import TestCase
from django.http import HttpRequest

from accounting.utils import is_ajax


class UtilsTestCase(TestCase):
    def test_is_ajax(self):
        request = HttpRequest()
        request.META['HTTP_X_Requested_With'] = 'XMLHttpRequest'

        self.assertTrue(is_ajax(request))
