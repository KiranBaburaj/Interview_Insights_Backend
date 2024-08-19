# employer/views.py

from rest_framework.exceptions import PermissionDenied
from .models import Company
from users.models import Employer
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions,generics,viewsets

class IsEmployerOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow admins to list and create
        if request.user.is_staff:
            return True
        # For non-admins, only allow if they are an employer
        return hasattr(request.user, 'employer')

    def has_object_permission(self, request, view, obj):
        # Allow admins full access
        if request.user.is_staff:
            return True
        # For non-admins, only allow if they own the company
        return obj.employer == request.user.employer



class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Company.objects.all()
        return Company.objects.filter(employer=self.request.user.employer)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            employer=self.request.user.employer
            serializer.save(employer=self.request.user.employer)
            employer.company_details_submitted = True
            employer.save()
        else:
            serializer.save()