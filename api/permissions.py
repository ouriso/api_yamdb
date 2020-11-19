from rest_framework import permissions


class IsAuthorOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'PATCH':
            return obj.author.is_admin or obj.author == request.user
        if request.method == 'DELETE':
            return (obj.author == request.user or
                    request.user.is_admin or
                    request.user.is_moderator or
                    request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin or request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin or request.user.is_superuser
