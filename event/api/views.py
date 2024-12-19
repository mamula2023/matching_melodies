from rest_framework import viewsets, permissions, response, status
from rest_framework.response import Response
from event.models import Event, Category, Genre
from event.serializers import EventSerializer
from event.permissions import EventPermissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [EventPermissions]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['genres', 'categories', 'author', 'city', 'event_type']
    ordering_fields = ['created_at', 'payment', 'title']  # todo add date after addint it go model itself
    ordering = ['created_at']


    def create(self, request, *args, **kwargs):
        role = request.user.role

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

