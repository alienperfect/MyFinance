from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import JsonResponse

from accounting.models import AccountingUnit, Category
from accounting.forms import AccountingUnitForm, CategoryForm


class RelatedCategoryMixin:
    """Mixin for creating categories on accounting page."""
    categories = []

    def post(self, request, *args, **kwargs):
        # Handle AJAX call
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            name = request.POST.get('name')
            category = Category(name=name)
            category.save()
            self.categories.append(category)
            return JsonResponse({'id': category.id})
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if self.categories:
            # Differentiate between Create and Update.
            # When self.object is None -- it's Createview.
            # Save it before adding relations.
            if not self.object:
                form.save()
            form.instance.category.add(*self.categories)
        return super().form_valid(form)


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
