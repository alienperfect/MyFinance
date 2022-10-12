from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from accounting.views import (
    ExpensesUnitListView, ExpensesUnitCreateView, ExpensesUnitUpdateView,
    IncomeUnitCreateView, IncomeUnitUpdateView, IncomeUnitListView,
    UnitListView, AccountingUnitDetailView, AccountingUnitDownloadView,
    CategoryCreateView, CategoryUpdateView, CategoryListView, CategoryDetailView,
    )

app_name = 'accounting'
urlpatterns = [
    path('', UnitListView.as_view(), name='unit-list'),

    path('expenses/', ExpensesUnitListView.as_view(), name='expenses-unit-list'),
    path('expenses_new/', ExpensesUnitCreateView.as_view(), name='expenses-unit-create'),
    path('expenses_edit/<int:pk>', ExpensesUnitUpdateView.as_view(), name='expenses-unit-update'),
    path('income/', IncomeUnitListView.as_view(), name='income-unit-list'),
    path('income_new/', IncomeUnitCreateView.as_view(), name='income-unit-create'),
    path('income_edit/<int:pk>', IncomeUnitUpdateView.as_view(), name='income-unit-update'),

    path('<int:pk>', AccountingUnitDetailView.as_view(), name='unit-detail'),
    path('download/<str:format>', AccountingUnitDownloadView.as_view(), name='unit-download'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category_new/', CategoryCreateView.as_view(), name='category-create'),
    path('category_edit/<int:pk>', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
