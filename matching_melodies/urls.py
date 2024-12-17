from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/user/', include('user.api.urls')),
    path('user/', include('user.urls')),

    path('api/event/', include('event.api.urls')),
    path('event/', include('event.urls')),

    
    path('api/application/', include('application.api.urls')),
    path('application/', include('application.urls')),


    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
