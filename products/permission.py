from rest_framework import permissions

class OwnerRightOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.is_authenticated:
            return request.user == obj.customer
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.customer
