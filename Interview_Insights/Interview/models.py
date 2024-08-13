# models.py
from django.db import models
from django.utils import timezone
from users.models import JobSeeker,Employer
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
    


    
class InterviewFeedback(models.Model):
    STAGE_CHOICES = [
        ('application_screening', 'Application Screening'),
        ('phone_interview', 'Phone Interview'),
        ('technical_assessment', 'Technical Assessment'),
        ('first_round_interview', 'First Round Interview'),
        ('second_round_interview', 'Second Round Interview'),
        ('hr_interview', 'HR Interview'),
        ('final_interview', 'Final Interview'),
        ('job_offer', 'Job Offer'),
        ('hired', 'Hired'),
    ]
    interview_schedule = models.OneToOneField(InterviewSchedule, related_name='feedback', on_delete=models.CASCADE)
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, unique=True)
    feedback = models.TextField(blank=True, null=True)
    score = models.PositiveIntegerField(default=0)  # You can set a max value if needed (e.g., max_value=100)
    provided_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)  # New field to indicate approval



    def __str__(self):
        return f"Feedback by {self.employer.user.email} for {self.job_seeker.user.email} on stage {self.stage.name}"
