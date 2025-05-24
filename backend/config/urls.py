from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from smartbin.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('', RedirectView.as_view(url='http://localhost:3000', permanent=True)),  # Redirection vers le frontend
    path('admin/', admin.site.urls),
    path('api/', include('smartbin.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 