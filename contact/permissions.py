from rest_framework import permissions
from user.models import UserModel

class IsAdminOrShopkeeper(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.role == UserModel.Role.SHOPKEEPER:
                return True
        return False