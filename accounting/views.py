from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import JsonResponse

from accounting.models import AccountingUnit, Category
from accounting.forms import AccountingUnitForm, CategoryForm
from accounting.utils import is_ajax, dump_to_xlsx, dump_to_csv 


class RelatedCategoryMixin:
    """Mixin for creating categories on accounting page."""
    categories = []

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
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
        XLSX = 'xlsx'
        CSV = 'csv'

        format = kwargs.get('format', '')
        if format in XLSX:
            response = dump_to_xlsx(request)
        elif format in CSV:
            response = dump_to_csv(request)
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
