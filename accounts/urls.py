from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from accounts.views import LoginView, CategoryCreateView, CategoryDetailView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
