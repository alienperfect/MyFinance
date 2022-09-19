from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='main'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounting/', include('accounting.urls', namespace='accounting')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
