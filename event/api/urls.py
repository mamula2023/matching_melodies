from django.urls import path, include
from .views import EventViewSet, ApplicationViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
        path('', EventViewSet.as_view({'post': 'create', 'get': 'list'}), name='event'),
        path('<int:pk>/', EventViewSet.as_view({'get': 'retrieve'}), name='event'),
        
        path('<int:pk>/apply/', ApplicationViewSet.as_view({'post': 'create'}), name='application'),
        path('<int:pk>/application/', ApplicationViewSet.as_view({'get': 'list'}), name='event-applications'),
        path('application/<int:pk>/', ApplicationViewSet.as_view({'get': 'retrieve'}), name='application'),

]

