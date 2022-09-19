from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import HttpResponse, HttpResponseNotFound

from accounting.models import AccountingUnit, Category
from accounting.forms import AccountingUnitForm, CategoryCreateForm, CategoryUpdateForm


def endpoint(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            name = request.POST.get('name', '')
            pk = request.POST.get('pk', '')

            category = Category(name=name)
            category.save()
            accounting_unit = AccountingUnit.objects.get(pk=pk)
            category.accountingunit_set.add(accounting_unit)
            return HttpResponse(category)
    return HttpResponseNotFound()


class AccountingUnitCreateView(CreateView):
    template_name = 'accounting/unit_create.html'
    model = AccountingUnit
    form_class = AccountingUnitForm
    success_url = reverse_lazy('accounting:unit-list')


class AccountingUnitUpdateView(UpdateView):
    template_name = 'accounting/unit_update.html'
    model = AccountingUnit
    form_class = AccountingUnitForm
    success_url = reverse_lazy('accounting:unit-list')


class AccountingUnitListView(ListView):
    template_name = 'accounting/unit_list.html'
    model = AccountingUnit


class AccountingUnitDetailView(DetailView):
    template_name = 'accounting/unit_detail.html'
    model = AccountingUnit


class CategoryCreateView(CreateView):
    template_name = 'accounting/category_create.html'
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('accounting:category-list')


class CategoryUpdateView(UpdateView):
    template_name = 'accounting/category_update.html'
    model = Category
    form_class = CategoryUpdateForm
    success_url = reverse_lazy('accounting:category-list')


class CategoryListView(ListView):
    template_name = 'accounting/category_list.html'
    model = Category


class CategoryDetailView(DetailView):
    template_name = 'accounting/category_detail.html'
    model = Category
