# employer/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job, JobCategory
from .serializers import JobSerializer, JobCategorySerializer
from .permissions import IsEmployerOwnerOrAdmin

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdmin]

    # Explicitly define the queryset attribute
    queryset = Job.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Job.objects.all()
        if not hasattr(self.request.user, 'employer'):
            return Job.objects.all()
        return Job.objects.filter(employer=self.request.user.employer)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(employer=self.request.user.employer)
        else:
            serializer.save()

class JobCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdmin]

    # Explicitly define the queryset attribute
    queryset = JobCategory.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return JobCategory.objects.all()
        return JobCategory.objects.all()

    def perform_create(self, serializer):
        serializer.save()


# views.py

from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import JobApplication
from users.models import JobSeeker
from .serializers import JobApplicationSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        job_seeker=self.request.user.jobseeker
        serializer.save(job_seeker=job_seeker)
