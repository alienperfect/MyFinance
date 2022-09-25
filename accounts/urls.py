from django.urls import path

from accounts.views import RegistrationView, LoginView, LogoutView, AccountUpdateView, AccountDetailView

app_name = 'accounts'
urlpatterns = [
    path('', AccountDetailView.as_view(), name='account-detail'),
    path('update/', AccountUpdateView.as_view(), name='account-update'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
