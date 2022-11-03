from django import forms
from accounting.models import ExpensesUnit, IncomeUnit, Category


class ExpensesUnitForm(forms.ModelForm):
    price = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''}))
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    quantity = forms.IntegerField(initial=1, widget=forms.TextInput(attrs={'numval': ''}))

    class Meta:
        model = ExpensesUnit
        exclude = ['created', 'modified', 'total_price']

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if data < 1:
            raise forms.ValidationError('Can be 1 or greater.')

        return data


class IncomeUnitForm(forms.ModelForm):
    income = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''}))
    receive_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    quantity = forms.IntegerField(initial=1, widget=forms.TextInput(attrs={'numval': ''}))

    class Meta:
        model = IncomeUnit
        exclude = ['created', 'modified', 'total_income']

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if data < 1:
            raise forms.ValidationError('Can be 1 or greater.')

        return data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
