from django import forms
from accounting.models import Category


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
