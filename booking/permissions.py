from rest_framework import permissions

class IsBusinessOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.groups.filter(name = 'business').exists()
