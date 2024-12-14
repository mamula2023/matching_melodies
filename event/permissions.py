from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class EventPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user.is_authenticated

        if view.action == 'create' and request.user.is_authenticated:
            author = request.data.get('author')
            if author is None:
                # author in fact, should not be sent, serializer is going to 
                # take author from request.user
                return True
            if str(author) != str(request.user.id):
                raise PermissionDenied("You can only create events authored by you!")
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, CustomUser):
            return obj == request.user

        return False

