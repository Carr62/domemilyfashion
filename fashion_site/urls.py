# fashion_site/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("fashion.urls")),
]

# This block is crucial for images to show in development
if settings.DEBUG:
    # Serve uploaded media (Product images)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static design files (About page images) <--- THIS WAS MISSING
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)