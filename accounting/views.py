import os
from typing import Callable

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import JsonResponse, HttpRequest, HttpResponse

from accounting.models import AccountingUnit, Category
from accounting.forms import AccountingUnitForm, CategoryForm
from accounting import utils


class RelatedCategoryMixin:
    """Mixin for creating categories on accounting page."""
    categories = []

    def post(self, request, *args, **kwargs):
        if utils.is_ajax(request):
            category = Category.objects.create(name=request.POST.get('name'))
            self.categories.append(category)
            return JsonResponse({'id': category.id})
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.object and self.categories:
            self.object.categories.add(*self.categories)
        return response


class AccountingUnitCreateView(RelatedCategoryMixin, CreateView):
    template_name = 'accounting/unit_create.html'
    model = AccountingUnit
    form_class = AccountingUnitForm
    success_url = reverse_lazy('accounting:unit-list')


class AccountingUnitUpdateView(RelatedCategoryMixin, UpdateView):
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


class AccountingUnitDownloadView(ListView):
    """View for downloading AccountingUnit data."""
    def get(self, request, *args, **kwargs):
        func_name: str = f'dump_to_{kwargs.get("format", "xlsx")}'
        statistics_func: Callable[[HttpRequest], dict] = getattr(utils, func_name)
        statistics_data = statistics_func(request)

        with open(statistics_data.get('full_path'), 'rb') as f:
            response = HttpResponse(f.read(), content_type=statistics_data.get('content_type'))
            response['Content-Disposition'] = f'filename={statistics_data.get("content_disposition")}'

        return response


class CategoryCreateView(CreateView):
    template_name = 'accounting/category_create.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('accounting:category-list')


class CategoryUpdateView(UpdateView):
    template_name = 'accounting/category_update.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('accounting:category-list')


class CategoryListView(ListView):
    template_name = 'accounting/category_list.html'
    model = Category


class CategoryDetailView(DetailView):
    template_name = 'accounting/category_detail.html'
    model = Category
