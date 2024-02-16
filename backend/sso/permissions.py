from rest_framework.permissions import BasePermission

class IsKISA(BasePermission):
    def has_permission(self, request, view):
        return request.user is not None and request.user.is_authenticated and request.user.is_kisa()

class IsKISAVerified(IsKISA):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_verified(request)