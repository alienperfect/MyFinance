from django import template
from django.urls import reverse_lazy
from django.db import models

register = template.Library()

@register.simple_tag
def get_unit_update_url(instance: models.Model) -> str:
    """Return url to the appropriate unit update view."""
    url = reverse_lazy('accounting:income-unit-update', kwargs={'pk': instance.pk})
    if instance.__class__.__name__.startswith('Expenses'):
        url = reverse_lazy('accounting:expenses-unit-update', kwargs={'pk': instance.pk})

    return url
