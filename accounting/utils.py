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


def dump_to_xlsx(request: HttpRequest) -> HttpResponse:
    """Dump AccountingUnit data to xlsx file and return response."""
    user_path = user_directory_path(request.user, 'any_filename_will_do')
    full_path = os.path.join(settings.MEDIA_ROOT, user_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    workbook = xlsxwriter.Workbook(full_path, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()

    headers = [
        'id',
        'name',
        'price',
        'created',
        'purchase_date',
        'categories__name',
    ]

    instances = AccountingUnit.objects.all().values(*headers)
    row = col = 0

    for header in headers:
        worksheet.write(row, col, header)
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

    with open(full_path, 'rb') as f:
        response = HttpResponse(
            f.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': 'attachment; filename="accounting.xlsx"'},
            )

        return response


def dump_to_csv(request: HttpRequest) -> HttpResponse:
    """Dump AccountingUnit data to csv file and return response."""
    user_path = user_directory_path(request.user, 'any_filename_will_do')
    full_path = os.path.join(settings.MEDIA_ROOT, user_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    headers = [
        'id',
        'name',
        'price',
        'created',
        'purchase_date',
        'categories__name',
    ]

    instances = AccountingUnit.objects.all().values(*headers)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="accounting.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow([*headers])

    for instance in instances:
        row = []
        for key in instance:
            row.append(instance[key])
        writer.writerow(row)

    return response
