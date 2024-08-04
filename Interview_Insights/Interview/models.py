# models.py
from django.db import models
from django.utils import timezone
from jobs . models import  JobApplication
class InterviewSchedule(models.Model):
    job_application = models.ForeignKey(JobApplication, related_name='interview_schedules', on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    duration = models.DurationField(default=timezone.timedelta(hours=1))
    location = models.CharField(max_length=255, blank=True, null=True)  # Can be a physical address or a video call link
    notes = models.TextField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Interview for {self.job_application} at {self.scheduled_time}"