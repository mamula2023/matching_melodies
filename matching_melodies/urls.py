from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('api/user/', include('user.api.urls')),
    path('user/', include('user.urls')),

    path('api/event/', include('event.api.urls')),
    path('event/', include('event.urls')),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

] + debug_toolbar_urls()
