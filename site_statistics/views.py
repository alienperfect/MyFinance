import calendar

from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from site_statistics.forms import StatisticsForm
from site_statistics.utils import get_month_name, calculate_money, get_category_stats


class StatisticsView(TemplateView):
    template_name = 'site_statistics/main.html'

    def get(self, request, *args, **kwargs):
        form = StatisticsForm(request.GET)
        month_year = None
        if form.is_valid():
            month_year = form.cleaned_data['month_year']
            kwargs['month_year'] = [get_month_name(month_year.month), month_year.year]

        kwargs['form'] = StatisticsForm()
        kwargs['money_dict'] = calculate_money(month_year)
        kwargs['category_stats'] = get_category_stats(month_year)

        return super().get(request, *args, **kwargs)
