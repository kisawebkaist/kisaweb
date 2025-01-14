from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsKISA(BasePermission):
    def has_permission(self, request, view):
        return request.user != None and request.user.is_authenticated and request.user.is_kisa()

class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_verified(request)
    
class IsVerifiedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or super().has_permission(request, view)