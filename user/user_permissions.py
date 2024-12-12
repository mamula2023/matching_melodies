from rest_framework import permissions
from .models import CustomUser


class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):

        # allow anyone registering
        if view.action != 'create':
            # in case of other actions check if user is authenticated
            if request.user and request.user.is_authenticated:
                user_id = request.user.id
                user = CustomUser.objects.get(id=user_id)
                # show user list only to superuser
                if view.action == 'list':
                    return user.is_superuser == True
                elif view.action == 'retrieve':
                    return user.is_superuser == True or int(view.kwargs.get('pk')) == user.id
                else:
                    # allow manipulation only if instance is request user itself
                    return user == request.user
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, CustomUser):
            return obj == request.user

        return False
