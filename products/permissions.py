from rest_framework import permissions


class IsSuperUserBrowseableAPI(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.__class__.__name__ == 'SchemaView':
                return request.user.is_superuser
            else:
                return True
        return False


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a superuser, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                request.user and
                request.user.is_authenticated and
                request.user.is_superuser
        )
