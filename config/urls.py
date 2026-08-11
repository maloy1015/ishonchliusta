from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('', include('workers.urls')),
    path('', include('jobs.urls')),
    path('', include('ratings.urls')),
    path('', include('chat.urls')),
    path('', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
