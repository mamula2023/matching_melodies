from rest_framework import permissions

class ApplicationPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated           

        
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.event.author == request.user or obj.user == request.user

        if view.action in ['accept', 'reject']:
            return obj.event.author == request.user

        return False

