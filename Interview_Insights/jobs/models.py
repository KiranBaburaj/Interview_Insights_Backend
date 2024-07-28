from django.db import models
from django.utils import timezone
from users.models import Employer, JobSeeker  # Assuming Employer model exists in employers app

class JobCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    employer = models.ForeignKey(Employer, related_name='jobs', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    nice_to_have = models.TextField(blank=True, null=True)
    employment_type = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_remote = models.BooleanField(default=False)
    application_deadline = models.DateField(blank=True, null=True)
    posted_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='open')
    views_count = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    experience_level = models.CharField(max_length=50, blank=True, null=True)
    job_function = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

class JobCategoryRelation(models.Model):
    job = models.ForeignKey(Job, related_name='jobcategoryrelation_set', on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategory, related_name='jobs', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('job', 'category')

    def __str__(self):
        return f"{self.job.title} - {self.category.name}"


class ApplicationStage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class JobApplication(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeeker, related_name='applications', on_delete=models.CASCADE)
    resume_url = models.URLField(max_length=255, blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='applied')  # 'applied', 'reviewed', 'interviewed', 'offered', 'hired', 'rejected'
    applied_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    stage = models.ForeignKey(ApplicationStage, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('job', 'job_seeker') 

    def __str__(self):
        return f"{self.job_seeker.user.email} - {self.job.title}"