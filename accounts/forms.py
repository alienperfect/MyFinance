from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Account, User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username']


class AccountUpdateForm(forms.ModelForm):
    monthly_salary = forms.DecimalField(
        required=False,
        help_text='Set either this or hourly rate',
        widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''})
        )

    hourly_rate = forms.DecimalField(
        required=False,
        help_text='Set either this or monthly salary',
        widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''})
        )

    hours_worked = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': '0', 'numval': ''})
        )

    class Meta:
        model = Account
        fields = [
            'monthly_salary',
            'hourly_rate',
            'hours_worked',
        ]

UserForm = forms.modelform_factory(User, fields=('username', 'avatar', 'job_position'))
