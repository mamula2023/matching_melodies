from rest_framework import viewsets, permissions, response, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from user import user_permissions
from user.models import CustomUser
from user.serializers import CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [user_permissions.IsAuthenticatedUser]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"message": "CustomUser created successfully."}
        return response

    def retrieve(self, request, pk=None, **kwargs):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

