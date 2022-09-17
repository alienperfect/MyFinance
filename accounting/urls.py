from django.urls import path

from accounting.views import CategoryCreateView, CategoryListView, CategoryDetailView

app_name = 'accounting'
urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category_new/', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
]
