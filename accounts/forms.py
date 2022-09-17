from django import forms
from accounts.models import User


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

    total_earned = forms.DecimalField(
        required=False,
        help_text='Equals to monthly salary or hourly rate * hours',
        widget=forms.TextInput(attrs={'value': 0, 'class': 'form-control-plaintext', 'readonly': '', 'numval': ''})
        )

    class Meta:
        model = User
        fields = [
            'username',
            'avatar',
            'job_position',
            'monthly_salary',
            'hourly_rate',
            'hours_worked',
            'total_earned',
        ]
