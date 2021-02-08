from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kover.urls')),
    path('login/', include('login.urls')),
    path('accounts/', include('allauth.urls')),
]


