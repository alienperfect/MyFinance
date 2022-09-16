from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from accounting.models import Category
from accounting.forms import CategoryCreateForm


class CategoryCreateView(CreateView):
    template_name = 'accounting/category_create.html'
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('accounting:category-list')


class CategoryListView(ListView):
    template_name = 'accounting/category_list.html'
    model = Category


class CategoryDetailView(DetailView):
    template_name = 'accounting/category_detail.html'
    model = Category
