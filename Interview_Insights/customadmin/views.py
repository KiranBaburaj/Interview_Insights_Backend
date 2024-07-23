from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from users.models import Company
from .serializers import CompanySerializer
from rest_framework import viewsets
from users.models import User, JobSeeker, Employer, Recruiter, Company
from .serializers import UserSerializer, JobSeekerSerializer, EmployerSerializer, RecruiterSerializer, CompanySerializer

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []

    queryset = User.objects.all()
    serializer_class = UserSerializer

class JobSeekerViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer

class EmployerViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object().user
        user.is_active = not user.is_active
        user.save()
        return Response({'status': 'is_active toggled'}, status=status.HTTP_200_OK)

class RecruiterViewSet(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = []
    permission_classes = []
   

    @action(detail=True, methods=['post'])
    def toggle_approval(self, request, pk=None):
        company = self.get_object()
        company.is_approved = not company.is_approved
        company.save()
        status = 'approved' if company.is_approved else 'disapproved'
        return Response({'status': f'company {status}'})
