# employer/permissions.py

from rest_framework import permissions

class IsEmployerOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        """
        # Allow admins to list and create
        if request.user.is_staff:
            return True
        # For non-admins, only allow if they are an employer
        return hasattr(request.user, 'employer')

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the specific object.
        """
        # Allow admins full access
        if request.user.is_staff:
            return True
        # For non-admins, only allow access if they own the company
        return obj.employer == request.user.employer
