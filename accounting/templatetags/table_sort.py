from django import template
from urllib.parse import urlencode
from collections import OrderedDict

register = template.Library()

@register.simple_tag
def order_by(request, field, value, direction=''):
    request_copy = request.GET.copy()

    if field == 'order_by' and field in request_copy.keys():          
        if request_copy[field].startswith('-') and request_copy[field].lstrip('-') == value:
            request_copy[field] = value
        elif request_copy[field].lstrip('-') == value:
            return ''
        else:
            request_copy[field] = direction + value
    else:
        request_copy[field] = direction + value
    return urlencode(OrderedDict(sorted(request_copy.items())))

@register.simple_tag
def get_arrow(request, key):
    value = request.GET.get('order_by', '')
    filename = 'sort'

    if value and key in value:
        if value.startswith('-'):
            filename = 'sort-down'
        else:
            filename = 'sort-up'
    return f'http://127.0.0.1:8000/static/img/{filename}.svg'
