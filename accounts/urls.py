from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginView

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]
