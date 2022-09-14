from django.contrib.auth import views
from django.urls import reverse_lazy


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('main')
    redirect_authenticated_user = True