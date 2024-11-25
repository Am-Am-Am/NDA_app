from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from NDA_app import settings
from NDA_app.views import custom_404
import catalog.views


urlpatterns = [
    path('', catalog.views.IndexView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('catalog/', include('catalog.urls')),
    path('files/', include('files.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)

handler404 = custom_404