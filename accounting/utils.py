import os
import csv
import xlsxwriter

from django.conf import settings
from django.http import HttpRequest

from accounting.models import ExpensesUnit, IncomeUnit
from accounts.utils import user_directory_path


def is_ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True


def dump_to_xlsx(request: HttpRequest) -> dict:
    """Dump model's data to XLSX file."""
    model_dict = {'expenses': ExpensesUnit, 'income': IncomeUnit}

    for key in model_dict:
        if key in request.GET.get('model', ''):
            model = model_dict[key]
            file_name = key

    user_path = user_directory_path(request.user, 'file_name')
    full_path = os.path.join(settings.MEDIA_ROOT, user_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    workbook = xlsxwriter.Workbook(full_path, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()
    headers = [key.name for key in model._meta.get_fields()]
    instances = model.objects.values(*headers)

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

    return {
        'full_path': full_path,
        'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'content_disposition': f'attachment; filename="{file_name}.xlsx"',
        }


def dump_to_csv(request: HttpRequest) -> dict:
    """Dump model's data to CSV file."""
    model_dict = {'expenses': ExpensesUnit, 'income': IncomeUnit}

    for key in model_dict:
        if key in request.GET.get('model', ''):
            model = model_dict[key]
            file_name = key

    user_path = user_directory_path(request.user, 'file_name')
    full_path = os.path.join(settings.MEDIA_ROOT, user_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    headers = [key.name for key in model._meta.get_fields()]
    instances = model.objects.values(*headers)

    with open(full_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for instance in instances:
            row = []
            for key in instance:
                row.append(instance[key])
            writer.writerow(*[row])

    return {
        'full_path': full_path,
        'content_type': 'text/csv',
        'content_disposition': f'attachment; filename="{file_name}.csv"',
        }
