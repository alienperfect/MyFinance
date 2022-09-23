from django.contrib.auth import views
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect

from accounts.models import Account, User
from accounts.forms import RegistrationForm, AccountUpdateForm, UserForm


class UserRelatedMixin:
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)


class RegistrationView(CreateView):
    template_name = 'accounts/registration.html'
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('accounts:account-detail')

    def form_valid(self, form):
        response = super().form_valid(form)
        Account.objects.create(user=self.object)
        login(self.request, self.object)
        return response


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('main'))


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('main')
    redirect_authenticated_user = True


class AccountUpdateView(UserRelatedMixin, UpdateView):
    template_name = 'accounts/account_update.html'
    model = Account
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accounts:account-detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request == 'POST':
            context['user_form'] = UserForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        user_form = UserForm(self.request.POST, self.request.FILES, instance=self.request.user)
        if user_form.is_valid():
            user_form.save()
        return super().form_valid(form)


class AccountDetailView(UserRelatedMixin, DetailView):
    template_name = 'accounts/account_detail.html'
    model = Account
