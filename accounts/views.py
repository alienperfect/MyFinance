from django.contrib.auth import views
from django.http.response import HttpResponseRedirect


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    next_page = '/'
    redirect_authenticated_user = True
