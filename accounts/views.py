from django.contrib.auth import views
from django.views.generic import UpdateView, DetailView
from django.urls import reverse_lazy

from accounts.models import Account
from accounts.forms import AccountUpdateForm, UserFormSet


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('main')
    redirect_authenticated_user = True


class AccountUpdateView(UpdateView):
    template_name = 'accounts/account_update.html'
    model = Account
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accounts:account-detail')

    def get_object(self, queryset=None):
        return Account.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request == 'POST':
            context['formset'] = UserFormSet(self.request.POST)
        else:
            context['formset'] = UserFormSet()
        return context

    def form_valid(self, form):
        formset = UserFormSet(self.request.POST, self.request.FILES)
        if formset.is_valid():
            formset.save()
        return super().form_valid(form)


class AccountDetailView(DetailView):
    template_name = 'accounts/account_detail.html'
    model = Account

    def get_object(self, queryset=None):
        return Account.objects.get(pk=self.request.user.pk)
