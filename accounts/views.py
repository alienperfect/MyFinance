from django.views.generic import CreateView, DetailView
from django.contrib.auth import views
from django.urls import reverse_lazy
from accounts.models import Category
from accounts.forms import CategoryCreateForm


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('main')
    redirect_authenticated_user = True


class CategoryCreateView(CreateView):
    template_name = 'accounts/category_create.html'
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('main')


class CategoryDetailView(DetailView):
    template_name = 'accounts/category_detail.html'
    model = Category
