from django.urls import path
from .views import EventViewSet

urlpatterns = [
        path('', EventViewSet.as_view({'post': 'create', 'get': 'list'}), name='event'),
        path('<int:pk>/', EventViewSet.as_view({'get': 'retrieve'}), name='event'),
]



