from django.db import models
from django.utils import timezone

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

    def __str__(self):
        return self.name
    
    def approve(self):
        self.is_approved = True
        self.save()

class CompanyLocation(models.Model):
    company = models.ForeignKey(Company, related_name='locations', on_delete=models.CASCADE)
    #location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.company.name} - {self.location}"

class CompanySocialLink(models.Model):
    company = models.ForeignKey(Company, related_name='social_links', on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    url = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.company.name} - {self.platform}"

class JobCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    company = models.ForeignKey(Company, related_name='jobs', on_delete=models.CASCADE)
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
    job = models.ForeignKey(Job, related_name='categories', on_delete=models.CASCADE)
    category = models.ForeignKey(JobCategory, related_name='jobs', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('job', 'category')

    def __str__(self):
        return f"{self.job.title} - {self.category.name}"

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class JobSkillRequirement(models.Model):
    job = models.ForeignKey(Job, related_name='skills', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='jobs', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('job', 'skill')

    def __str__(self):
        return f"{self.job.title} - {self.skill.name}"

class ApplicationStage(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Ensure to add default stages
