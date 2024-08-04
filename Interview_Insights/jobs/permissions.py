from rest_framework import permissions

class IsEmployerOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow admins full access
        if request.user.is_staff:
            return True
        
        # For non-admins, check if they are an employer
        if hasattr(request.user, 'employer'):
            return True
        
        # For specific actions like list and retrieve, allow access for job seekers
        if view.action in ['list', 'retrieve']:
            return not hasattr(request.user, 'employer')
        
        # Default to deny access
        return False

    def has_object_permission(self, request, view, obj):
        # Allow admins full access
        if request.user.is_staff:
            return True
        
        # Check if the request user is the employer associated with the object
        if hasattr(request.user, 'employer'):
            return obj.employer == request.user.employer
        
        # Default to deny access
        return False
