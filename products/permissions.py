from rest_framework import permissions
from user.models import Role

class IsAdminOrShopkeeper(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.role == Role.SHOPKEEPER:
                return True
        return False