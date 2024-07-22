from django.shortcuts import render

# Create your views here.
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
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

class RecruiterViewSet(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
