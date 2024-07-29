from rest_framework import generics, permissions
from users.models import JobSeeker
from .serializers import JobSeekerSerializer

class JobSeekerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = JobSeekerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return JobSeeker.objects.get(user=self.request.user)

class JobSeekerListCreateAPIView(generics.ListCreateAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = [permissions.IsAdminUser]

class JobSeekerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = [permissions.IsAdminUser]