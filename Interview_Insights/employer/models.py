from django.db import models
from django.utils import timezone
from django.apps import apps
class Company(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField(max_length=255, blank=True, null=True)
    website_url = models.URLField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True, null=True)
    founded_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    headquarters_location = models.CharField(max_length=100, blank=True, null=True)
    employee_count = models.IntegerField(blank=True, null=True)
    tech_stack = models.JSONField(blank=True, null=True)  # Storing tech stack as a JSON field
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    gst_document = models.FileField(upload_to='gst_documents/', null=True)
    is_approved = models.BooleanField(default=False)
    employer = models.OneToOneField('users.Employer', on_delete=models.CASCADE, related_name='company')


    def __str__(self):
        return self.name
    
    def approve(self):
        self.is_approved = True
        self.save()

class CompanyLocation(models.Model):
    company = models.ForeignKey(Company, related_name='locations', on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default='default_location')

    def __str__(self):
        return f"{self.company.name} - {self.location}"

class CompanySocialLink(models.Model):
    company = models.ForeignKey(Company, related_name='social_links', on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    url = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.company.name} - {self.platform}"
