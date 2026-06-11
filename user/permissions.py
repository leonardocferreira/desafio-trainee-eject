from rest_framework import permissions

class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.id == obj.id:
                return True
        return False