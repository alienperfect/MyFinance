from django import forms
from accounting.models import AccountingUnit, Category


class AccountingUnitForm(forms.ModelForm):
    price = forms.DecimalField(
        help_text='per one',
        widget=forms.TextInput(attrs={'placeholder': '0.00', 'numval': ''}),
        )

    quantity = forms.IntegerField(initial=1, widget=forms.TextInput(attrs={'numval': ''}))
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = AccountingUnit
        exclude = ['total_price', 'created', 'modified']
    
    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        if data < 1:
            raise forms.ValidationError('Could be 1 or greater.')
        
        return data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
