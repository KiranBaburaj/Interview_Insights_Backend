# employer/permissions.py
from rest_framework import permissions

class IsEmployerOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow admins to list and create
        if request.user.is_staff:
            return True
        # Allow job seekers to view jobs
        if view.action in ['list', 'retrieve'] and not hasattr(request.user, 'employer'):
            return True
        # For non-admins, only allow if they are an employer
        return hasattr(request.user, 'employer')

    def has_object_permission(self, request, view, obj):
        # Allow admins full access
        if request.user.is_staff:
            return True
        # For non-admins, only allow if they own the company
        if hasattr(request.user, 'employer'):
            return obj.employer == request.user.employer
        return False
