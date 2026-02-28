from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/prayers/', include('apps.prayers.urls')),
    path('api/hopecasts/', include('apps.hopecasts.urls')),
    path('api/donations/', include('apps.donations.urls')),
    path('api/hope-ai/', include('apps.hope_ai.urls')),
]
