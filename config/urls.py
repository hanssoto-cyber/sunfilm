import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(os.environ.get('ADMIN_URL', 'admin/'), admin.site.urls),
    path('servicios/', include('servicios.urls')),
    path('galeria/', include('galeria.urls')),
    path('tips/', include('blog.urls')),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)