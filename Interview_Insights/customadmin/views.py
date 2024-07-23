from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
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
