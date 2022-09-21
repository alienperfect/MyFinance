from django import forms
from accounting.models import AccountingUnit, Category


class AccountingUnitForm(forms.ModelForm):
    price = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''}))
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = AccountingUnit
        exclude = ['created', 'modified']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
