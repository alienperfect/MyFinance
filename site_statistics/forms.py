from django import forms


class StatisticsForm(forms.Form):
    month_year = forms.DateField(input_formats=['%m/%Y'], label='Month')
