from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from accounting.views import AccountingUnitCreateView, AccountingUnitUpdateView, AccountingUnitListView, AccountingUnitDetailView, CategoryCreateView, CategoryUpdateView, CategoryListView, CategoryDetailView

app_name = 'accounting'
urlpatterns = [
    path('', AccountingUnitListView.as_view(), name='unit-list'),
    path('new/', AccountingUnitCreateView.as_view(), name='unit-create'),
    path('edit/<int:pk>', AccountingUnitUpdateView.as_view(), name='unit-update'),
    path('<int:pk>', AccountingUnitDetailView.as_view(), name='unit-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category_new/', CategoryCreateView.as_view(), name='category-create'),
    path('category_edit/<int:pk>', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
