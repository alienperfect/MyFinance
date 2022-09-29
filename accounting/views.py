from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import JsonResponse

from accounting.models import AccountingUnit, Category
from accounting.forms import AccountingUnitForm, CategoryForm
from accounting.utils import is_ajax


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


class SearchMixin:
    """Mixin for searching by model's fields. Requires filters dict to be set."""
    def get_queryset(self):
        request = self.request.GET
        values = {}
        for key in request:
            if request[key]:
                if self.filters[key].endswith('__in'):
                    values[self.filters[key]] = request.getlist(key)
                else:
                    values[self.filters[key]] = request[key]
        return self.model.objects.filter(**values).distinct()


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
    filters = {
        'name': 'name__icontains',
        'price': 'price',
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


class CategoryDetailView(DetailView):
    template_name = 'accounting/category_detail.html'
    model = Category
