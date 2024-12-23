from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
from .views import LoginView, SignUpView
from event.views import HomePageView

router = routers.DefaultRouter()

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(),
         name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/logout/', TokenBlacklistView.as_view(), name='token-logout'),

    path('login/', LoginView.as_view(), name='login-page'),
    path('signup/', SignUpView.as_view(), name='signup-page'),
    path('logout/', HomePageView.as_view(), name='logout-page'),
]
