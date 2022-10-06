import os
import csv
import xlsxwriter

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from accounting.models import AccountingUnit
from accounts.utils import user_directory_path


def is_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True


def dump_to_xlsx(request: HttpRequest) -> dict:
    """Dump AccountingUnit data to xlsx file and return dict."""
    user_path = user_directory_path(request.user, 'any_filename_will_do')
    full_path = os.path.join(settings.MEDIA_ROOT, user_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    content_disposition = 'attachment; filename="accounting.xlsx"'

    workbook = xlsxwriter.Workbook(full_path, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()

    headers = {
        'id': 'id',
        'name': 'name',
        'price': 'price',
        'created': 'created',
        'purchase_date': 'purchase date',
        'categories__name': 'categories',
    }

    instances = AccountingUnit.objects.values(*[val for val in headers])
    row = col = 0

    for header in headers:
        worksheet.write(row, col, headers[header])
        col += 1

    col = 0
    row += 1

    for instance in instances:
        for key in instance:
            worksheet.write(row, col, instance[key])
            col += 1
        col = 0
        row += 1

    workbook.close()

    return {'full_path': full_path, 'content_type': content_type, 'content_disposition': content_disposition}


def dump_to_csv(request: HttpRequest) -> HttpResponse:
    """Dump AccountingUnit data to csv file and return response."""
    user_path = user_directory_path(request.user, 'any_filename_will_do')
    full_path = os.path.join(settings.MEDIA_ROOT, user_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    content_type = 'text/csv'
    content_disposition = 'attachment; filename="accounting.csv"'

    headers = {
        'id': 'id',
        'name': 'name',
        'price': 'price',
        'created': 'created',
        'purchase_date': 'purchase date',
        'categories__name': 'categories',
    }

    instances = AccountingUnit.objects.values(*[val for val in headers])

    with open(full_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers[header] for header in headers)

        for instance in instances:
            row = []
            for key in instance:
                row.append(instance[key])
            writer.writerow(*[row])

    return {'full_path': full_path, 'content_type': content_type, 'content_disposition': content_disposition}
