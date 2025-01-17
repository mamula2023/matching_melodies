from rest_framework import viewsets, permissions, response, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from user import user_permissions
from user.models import CustomUser
from user.serializers import CustomUserSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [user_permissions.IsAuthenticatedUser]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['role']
    ordering_fields = ['created_at', 'username']
    ordering = ['created_at']


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"message": "CustomUser created successfully."}
        return response

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

