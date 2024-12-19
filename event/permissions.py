from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework import status

class EventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user.is_authenticated

        if view.action == 'create' and request.user.is_authenticated:
            author = request.data.get('author')
            event_type = request.data.get('event_type')
            if author is None:
                # author in fact, should not be sent, serializer is going to 
                # take author from request.user
                if event_type not in ['gig', 'collaboration']:
                    raise ParseError(f"event_type {event_type} not allowed", status.HTTP_400_BAD_REQUEST)

                if event_type == 'gig' and not request.user.role == 'organizer':
                    raise PermissionDenied("event with type of gig can only created by organizer")
                if event_type == 'collaboration' and not request.user.role == 'musician':
                    raise PermissionDenied("event with type of collaboration can only created by organizer")
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

