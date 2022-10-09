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


class SearchMixin:
    """Mixin for searching by model's fields. Requires filters and ordering to be set."""
    ordering: str = None

    def get_queryset(self):
        request_data = self.request.GET
        values = {}

        for key in request_data:
            if not request_data[key]:
                continue

            if key.startswith('order_by'):
                self.ordering = request_data[key]
            elif self.filters[key].endswith('__in'):
                values[self.filters[key]] = request_data.getlist(key)
            else:
                values[self.filters[key]] = request_data[key]

        return self.model.objects.filter(**values).order_by(self.ordering).distinct()


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


class AccountingUnitListView(SearchMixin, ListView):
    template_name = 'accounting/unit_list.html'
    model = AccountingUnit
    ordering = 'created'

    filters = {
        'name': 'name__icontains',
        'total_price': 'total_price',
        'purchase_date': 'purchase_date',
        'created': 'created__date',
        'categories': 'categories__name__in',
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


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


class CategoryListView(SearchMixin, ListView):
    template_name = 'accounting/category_list.html'
    model = Category

    filters = {
        'name': 'name__icontains',
        'created': 'created__date',
        }

    ordering = 'created'


class CategoryDetailView(DetailView):
    template_name = 'accounting/category_detail.html'
    model = Category
