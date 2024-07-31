# employer/views.py

from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Job, JobCategory
from .serializers import JobSerializer, JobCategorySerializer
from .permissions import IsEmployerOwnerOrAdmin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import JobApplication
from .serializers import JobApplicationSerializer
from .filters import JobFilter,JobApplicationFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.none()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'location']  # Add fields you want to search

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdmin]
        return super().get_permissions()

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            queryset = Job.objects.all()
        elif self.request.user.is_staff:
            queryset = Job.objects.all()
        elif not hasattr(self.request.user, 'employer'):
            queryset = Job.objects.none()
        else:
            queryset = Job.objects.filter(employer=self.request.user.employer)
        
        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(employer=self.request.user.employer)
        else:
            serializer.save()

class JobCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdmin]

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
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import JobApplication
from .serializers import JobApplicationSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Handle multipart form data

    def perform_create(self, serializer):
        job_seeker = self.request.user.jobseeker
        serializer.save(job_seeker=job_seeker)


class CheckApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        job_seeker = self.request.user.jobseeker
        has_applied = JobApplication.objects.filter(job_seeker=job_seeker, job_id=job_id).exists()
        return Response({'hasApplied': has_applied})


# Add the necessary imports at the beginning of your views.py file
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Job, JobApplication
from .serializers import JobApplicationSerializer

@api_view(['GET'])
def job_applicants(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        applicants = JobApplication.objects.filter(job=job)
        serializer = JobApplicationSerializer(applicants, many=True)
        return Response(serializer.data)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)



class JobApplicationList(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobApplicationFilter  # Add the filterset class

    def get_queryset(self):
        user = self.request.user
        return JobApplication.objects.filter(job_seeker__user=user)