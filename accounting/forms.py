from django import forms
from accounting.models import ExpensesUnit, IncomeUnit, Category


class ExpensesUnitForm(forms.ModelForm):
    price = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''}))
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ExpensesUnit
        exclude = ['created', 'modified']


class IncomeUnitForm(forms.ModelForm):
    income = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''}))
    receive_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = IncomeUnit
        exclude = ['created', 'modified']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
