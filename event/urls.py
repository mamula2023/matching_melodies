from django.urls import path
from .views import HomePageView, AboutView, ContactView, EventView, EventCreateView

urlpatterns = [
    path('events', HomePageView.as_view(), name='events'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('<int:pk>/', EventView.as_view(), name='event-detail'),
    path('create/', EventCreateView.as_view(), name='create-event'),
]

