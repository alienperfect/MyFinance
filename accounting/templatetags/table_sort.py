import os
from urllib.parse import urlencode
from collections import OrderedDict

from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def order_by(request, field, value, direction='', model=None):
    request_copy = request.GET.copy()

    if field == 'order_by' and field in request_copy.keys():          
        if request_copy[field].startswith('-') and request_copy[field].lstrip('-') == value:
            request_copy[field] = value
        elif request_copy[field].lstrip('-') == value:
            if model:
                querystring = f'model={model}'
            else:
                querystring = ''
            return querystring
        else:
            request_copy[field] = direction + value
    else:
        request_copy[field] = direction + value
    return urlencode(OrderedDict(sorted(request_copy.items())))

@register.simple_tag
def get_arrow(request, key):
    value = request.GET.get('order_by', '')
    filename = 'img/sort.svg'

    if value and key in value:
        if value.startswith('-'):
            filename = 'img/sort-down.svg'
        else:
            filename = 'img/sort-up.svg'

    return static(filename)
