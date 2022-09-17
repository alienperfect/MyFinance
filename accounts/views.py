from django.contrib.auth import views
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from accounts.models import User
from accounts.forms import AccountUpdateForm

class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('main')
    redirect_authenticated_user = True


class AccountUpdateView(UpdateView):
    template_name = 'accounts/account_update.html'
    model = User
    form_class = AccountUpdateForm
    success_url = reverse_lazy('accounts:account-update')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        if form.instance.hourly_rate and form.instance.hours_worked:
            form.instance.total_earned = form.instance.hourly_rate * form.instance.hours_worked
        elif form.instance.monthly_salary:
            form.instance.total_earned = form.instance.monthly_salary
        else:
            form.instance.total_earned = 0
        return super().form_valid(form)
