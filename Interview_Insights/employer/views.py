# employer/views.py

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Company
from .serializers import CompanySerializer

class IsAdminEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'employer') and request.user.employer.company_role == 'admin'

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminEmployer]

    def perform_create(self, serializer):
        if not self.request.user.employer.can_manage_company():
            raise PermissionDenied("You do not have permission to add company details.")
        serializer.save()

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminEmployer]

    def perform_update(self, serializer):
        if not self.request.user.employer.can_manage_company():
            raise PermissionDenied("You do not have permission to edit this company.")
        serializer.save()
