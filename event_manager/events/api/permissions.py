from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    """
    REturn True, if user is object.author or die HTTP-Methode ist Save.
    """

    def has_object_permission(self, request, view, obj):
        is_owner = request.user == obj.author
        return is_owner or request.method in permissions.SAFE_METHODS
