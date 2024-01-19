from rest_framework.permissions import BasePermission

class IsKAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.kaist_profile.is_authenticated