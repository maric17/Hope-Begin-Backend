from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.role == 'admin':
            return True
        # Check if the user is the owner of the object
        return obj == request.user

class IsApproved(permissions.BasePermission):
    """
    Custom permission to only allow approved users to access the API.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_approved)
