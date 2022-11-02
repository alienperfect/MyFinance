from typing import Callable
from itertools import chain

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import JsonResponse, HttpRequest, HttpResponse

from accounting.models import ExpensesUnit, IncomeUnit, Category
from accounting.forms import ExpensesUnitForm, IncomeUnitForm, CategoryForm
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


class SingleObjectSearchMixin:
    """Mixin for searching and ordering on a model."""
    filters: dict = None
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


class MultipleObjectSearchMixin:
    """Mixin for searching and ordering on multiple models."""
    filters: dict = None
    ordering: str = None
    model_list: list = None

    def get_queryset(self):
        request_data = self.request.GET
        values = {}
        queryset = {}

        for model in self.model_list:
            for key in request_data:
                if not request_data[key]:
                    continue
                
                fields = [field.name for field in model._meta.get_fields()]

                if key not in fields:
                    if key.startswith('order_by') and request_data[key].replace('-', '') in fields:
                        self.ordering = request_data[key]
                    continue

                elif self.filters[key].endswith('__in'):
                    values[self.filters[key]] = request_data.getlist(key)
                else:
                    values[self.filters[key]] = request_data[key]

            queryset[model.__name__] = model.objects.filter(**values).order_by(self.ordering).distinct()
            values.clear()
            self.ordering = '-created'

        return queryset


class ExpensesUnitCreateView(RelatedCategoryMixin, CreateView):
    template_name = 'accounting/unit_create.html'
    model = ExpensesUnit
    form_class = ExpensesUnitForm
    success_url = reverse_lazy('accounting:unit-list')


class IncomeUnitCreateView(RelatedCategoryMixin, CreateView):
    template_name = 'accounting/unit_create.html'
    model = IncomeUnit
    form_class = IncomeUnitForm
    success_url = reverse_lazy('accounting:unit-list')


class ExpensesUnitUpdateView(RelatedCategoryMixin, UpdateView):
    template_name = 'accounting/unit_update.html'
    model = ExpensesUnit
    form_class = ExpensesUnitForm
    success_url = reverse_lazy('accounting:unit-list')


class IncomeUnitUpdateView(RelatedCategoryMixin, UpdateView):
    template_name = 'accounting/unit_update.html'
    model = IncomeUnit
    form_class = IncomeUnitForm
    success_url = reverse_lazy('accounting:unit-list')


class UnitListMixin:
    """Mixin for all UnitListView classes."""

    filters = {
        'name': 'name__icontains',
        'created': 'created__date',
        'categories': 'categories__name__in',
        'price': 'price',
        'purchase_date': 'purchase_date',
        'income': 'income',
        'receive_date': 'receive_date',
        }

    ordering = '-created'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class UnitListView(UnitListMixin, MultipleObjectSearchMixin, ListView):
    template_name = 'accounting/unit_list.html'
    model_list = [ExpensesUnit, IncomeUnit]
    context_object_name = 'unit_list'


class ExpensesUnitListView(UnitListMixin, SingleObjectSearchMixin, ListView):
    template_name = 'accounting/expenses_unit_list.html'
    model = ExpensesUnit


class IncomeUnitListView(UnitListMixin, SingleObjectSearchMixin, ListView):
    template_name = 'accounting/income_unit_list.html'
    model = IncomeUnit


class AccountingUnitDetailView(DetailView):
    template_name = 'accounting/expenses_unit_detail.html'
    model = ExpensesUnit


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


class CategoryListView(SingleObjectSearchMixin, ListView):
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
