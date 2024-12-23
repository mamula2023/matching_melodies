from rest_framework import viewsets, permissions, response, status
from rest_framework.response import Response
from event.models import Event, Category, Genre
from event.serializers import EventSerializer, CategorySerializer, GenreSerializer
from event.permissions import EventPermissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from user.models import CustomUser
from rest_framework.permissions import IsAuthenticated

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [EventPermissions]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['genres', 'categories', 'author', 'city', 'event_type']
    ordering_fields = ['created_at', 'payment', 'title', 'date'] 
    ordering = ['created_at']


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            events = self.get_serializer(page, many=True).data
            paginated_response = self.get_paginated_response(events)
        else:
            events = self.get_serializer(queryset, many=True).data
            paginated_response = Response({'events': events})

        cities = queryset.values_list('city', flat=True).distinct()
        genres = Genre.objects.filter(events__in=queryset).distinct().values("id", "title")
        categories = Category.objects.filter(events__in=queryset).distinct().values("id", "title")

        authors = CustomUser.objects.filter(events__in=queryset).distinct().values("id", "username")

        paginated_response.data['filters'] = {
            'cities': list(set(cities)),
            'genres': list(genres),
            'categories': list(categories),
            'authors': list(authors),
        }

        return paginated_response

    def create(self, request, *args, **kwargs):
        role = request.user.role
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    model = Category
    pagination_class = None
    
    @method_decorator(cache_page(60*60*6))
    def list(self, request):
        return super().list(request)
    
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer 
    pagination_class = None
    model = Genre

    @method_decorator(cache_page(60*60*6))
    def list(self, request):
        return super().list(request)


