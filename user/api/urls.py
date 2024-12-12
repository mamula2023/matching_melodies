from django.urls import path

from user.api.views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create'}), name='user'),
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
]
