from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.http import HttpResponseRedirect, HttpResponse

from accounting.models import AccountingUnit, Category
from accounting.forms import AccountingUnitForm, CategoryCreateForm, CategoryUpdateForm


class RelatedCategoryMixin:
    def __init__(self):
        self.categories = []

    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            name = request.POST.get('name')
            category = Category(name=name)
            category.save()
            self.categories.append(category)
            return HttpResponse()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        if self.categories:
            for category in self.categories:
                form.instance.category.add(category)
            form.save()
        return HttpResponseRedirect(self.success_url)


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
