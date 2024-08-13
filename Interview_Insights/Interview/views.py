# views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import InterviewSchedule, JobApplication
from .serializers import InterviewScheduleSerializer
from jobs.permissions import IsEmployerOwnerOrAdmin

class ScheduleInterviewView(generics.CreateAPIView):
    serializer_class = InterviewScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job_application = serializer.validated_data['job_application']
        scheduled_time = serializer.validated_data['scheduled_time']
        duration = serializer.validated_data['duration']

        # Check permissions
        if job_application.job.employer.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to schedule an interview for this application.")

        # Check if an interview already exists for this job application
        if InterviewSchedule.objects.filter(job_application=job_application).exists():
            raise ValidationError("An interview is already scheduled for this job application.")

        # Check for time conflicts
        end_time = scheduled_time + duration
        conflicting_interviews = InterviewSchedule.objects.filter(
            Q(scheduled_time__lt=end_time) & Q(scheduled_time__gte=scheduled_time) |
            Q(scheduled_time__lte=scheduled_time, scheduled_time__gt=end_time)
        )

        if conflicting_interviews.exists():
            raise ValidationError("This time slot conflicts with an existing interview.")

        serializer.save()

class UpdateInterviewScheduleView(generics.UpdateAPIView):
    queryset = InterviewSchedule.objects.all()
    serializer_class = InterviewScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.job_application.job.employer.user != self.request.user and not self.request.user.is_staff:
            raise permissions.PermissionDenied("You don't have permission to update this interview schedule.")
        return obj

    def perform_update(self, serializer):
        scheduled_time = serializer.validated_data.get('scheduled_time')
        duration = serializer.validated_data.get('duration')

        if scheduled_time and duration:
            end_time = scheduled_time + duration
            conflicting_interviews = InterviewSchedule.objects.filter(
                Q(scheduled_time__lt=end_time) & Q(scheduled_time__gte=scheduled_time) |
                Q(scheduled_time__lte=scheduled_time, scheduled_time__gt=end_time)
            ).exclude(pk=self.get_object().pk)

            if conflicting_interviews.exists():
                raise ValidationError("This time slot conflicts with an existing interview.")

        serializer.save()

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
    

from rest_framework import viewsets
from .models import InterviewFeedback
from .serializers import InterviewFeedbackSerializer
from rest_framework import viewsets, permissions

class InterviewFeedbackViewSet(viewsets.ModelViewSet):
    queryset = InterviewFeedback.objects.all()
    serializer_class = InterviewFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned feedbacks to those related to the current user's job applications.
        """
        queryset = super().get_queryset()
        user = self.request.user
        return queryset.filter(interview_schedule__job_application__job_seeker__user=user)
