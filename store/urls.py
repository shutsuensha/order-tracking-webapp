from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import google_one_tap_login

urlpatterns = [
    path('', include('core.urls')),
    path('items/', include('item.urls')),
    path('admin/', admin.site.urls),
    path('inbox/', include('conversation.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('google_one_tap_login/', google_one_tap_login, name='google_one_tap_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)