from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from employer.models import Company
from rest_framework import viewsets
from users.models import User, JobSeeker, Employer, Recruiter, Company
from .serializers import UserSerializer, JobSeekerSerializer, EmployerSerializer, RecruiterSerializer
from employer.serializers import CompanySerializer
from django.core.mail import send_mail
from django.conf import settings
from jobs.models import Job


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
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        job_seeker = self.get_object()
        user = job_seeker.user
        user.is_active = not user.is_active
        user.save()
        return Response({'status': 'is_active toggled'}, status=status.HTTP_200_OK)

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
        serializer = CompanySerializer(company)
        
        # Send email notification
        subject = ''
        message = ''
        recipient_list = [company.employer.user.email]

        if company.is_approved:
            subject = 'Your Company has been Approved'
            message = f'Hello {company.name},\n\nWe are pleased to inform you that your company has been approved.\n\nBest regards,\nYour Team'
            Job.objects.filter(employer=company.employer).update(is_active=True)
        else:
            # If company is disapproved, revoke permission to post jobs and disable all existing jobs
            subject = 'Your Company has been Disapproved'
            message = f'Hello {company.name},\n\nUnfortunately, your company has been disapproved. All your existing job posts have been disabled, and you no longer have permission to post jobs.\n\nBest regards,\nYour Team'
            
            # Disable all jobs associated with the company
            Job.objects.filter(employer=company.employer).update(is_active=False)

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
        
        return Response(serializer.data)
