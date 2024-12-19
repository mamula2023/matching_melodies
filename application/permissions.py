from rest_framework import permissions

class ApplicationPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return True

        
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.event.author == request.user or obj.user == request.user

        if view.action in ['accept', 'reject']:
            return obj.event.author == request.user

        return False

