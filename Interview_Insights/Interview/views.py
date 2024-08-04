# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import InterviewSchedule, JobApplication
from .serializers import InterviewScheduleSerializer
from  jobs.permissions import IsEmployerOwnerOrAdmin

class ScheduleInterviewView(generics.CreateAPIView):
    serializer_class = InterviewScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOwnerOrAdmin]

    def perform_create(self, serializer):
        job_application = serializer.validated_data['job_application']
        if job_application.job.employer.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to schedule an interview for this application.")
        serializer.save()

class UpdateInterviewScheduleView(generics.UpdateAPIView):
    queryset = InterviewSchedule.objects.all()
    serializer_class = InterviewScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerOwnerOrAdmin]

    def get_object(self):
        obj = super().get_object()
        if obj.job_application.job.employer.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to update this interview schedule.")
        return obj

class ListInterviewSchedulesView(generics.ListAPIView):
    serializer_class = InterviewScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'employer'):
            return InterviewSchedule.objects.filter(job_application__job__employer=user.employer)
        elif hasattr(user, 'jobseeker'):
            return InterviewSchedule.objects.filter(job_application__job_seeker=user.jobseeker)
        elif user.is_staff:
            return InterviewSchedule.objects.all()
        return InterviewSchedule.objects.none()