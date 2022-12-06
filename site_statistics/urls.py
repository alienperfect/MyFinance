from django.urls import path

from site_statistics.views import StatisticsView

app_name = 'site_statistics'
urlpatterns = [
    path('', StatisticsView.as_view(), name='main'),
]
