from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts.views import LoginView, AccountUpdateView

app_name = 'accounts'
urlpatterns = [
    path('', AccountUpdateView.as_view(), name='account-update'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
