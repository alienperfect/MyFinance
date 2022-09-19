from django import forms
from accounting.models import AccountingUnit, Category
from accounting.widgets import DatePickerInput


class AccountingUnitForm(forms.ModelForm):
    price = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''}))

    class Meta:
        model = AccountingUnit
        exclude = ['created']

        widgets = {
            'purchase_date': DatePickerInput(),
        }


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
