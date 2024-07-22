from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Job, JobCategory
from .serializers import JobSerializer, JobCategorySerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user.employer)

class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [AllowAny]
