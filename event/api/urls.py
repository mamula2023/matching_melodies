from django.urls import path
from .views import EventViewSet, GenreViewSet, CategoryViewSet
from application.api.views import ApplicationViewSet

urlpatterns = [
    path('', EventViewSet.as_view({'post': 'create', 'get': 'list'}), name='event'),
    path('<int:pk>/', EventViewSet.as_view({'get': 'retrieve'}), name='event'),
    path('<int:pk>/apply/', ApplicationViewSet.as_view({'post': 'create'}), name='application'),

    path('<int:pk>/application/', ApplicationViewSet.as_view({'get': 'list'}), name='event-applications'),
    path('genre/', GenreViewSet.as_view({'get': 'list'}), name='genres-list'),
    path('category/', CategoryViewSet.as_view({'get':'list'}), name='categories-list'),
]

