from django.contrib.auth import views
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy

from accounts.models import Account
from accounts.forms import AccountUpdateForm, UserForm


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('main')
    redirect_authenticated_user = True


class UserRelatedMixin:
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)


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
