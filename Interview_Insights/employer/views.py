# employer/views.py

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class IsAdminEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'employer') and request.user.employer.company_role == 'admin'

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []

    def perform_create(self, serializer):
        if not self.request.user.employer.can_manage_company():
            raise PermissionDenied("You do not have permission to add company details.")
        serializer.save()

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []

    def perform_update(self, serializer):
        if not self.request.user.employer.can_manage_company():
            raise PermissionDenied("You do not have permission to edit this company.")
        serializer.save()

# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []  # Ensure only admins can access

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        company = self.get_object()
        company.is_approved = True
        company.save()
        return Response({'status': 'company approved'})
