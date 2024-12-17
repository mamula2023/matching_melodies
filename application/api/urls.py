from django.urls import path, include
from .views import ApplicationViewSet

urlpatterns = [
    path('<int:pk>/', ApplicationViewSet.as_view({'get': 'retrieve'}), name='application-retrieve'),
    path('<int:pk>/accept/', ApplicationViewSet.as_view({'post': 'accept'}), name='accept-application'),
    path('<int:pk>/reject/', ApplicationViewSet.as_view({'post': 'reject'}), name='reject-application')

]
