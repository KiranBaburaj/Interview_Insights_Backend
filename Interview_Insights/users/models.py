from django.db import models
from employer.models import Company

# Create your models here.
# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo_url = models.URLField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
    portfolio_url = models.URLField(max_length=255, null=True, blank=True)
    resume_url = models.URLField(max_length=255, null=True, blank=True)
    current_job_title = models.CharField(max_length=100, null=True, blank=True)
    job_preferences = models.TextField(blank=True, null=True)

class Employer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True)
    company_role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('manager', 'Manager')], default='admin')
    def can_manage_company(self):
        return self.company_role == 'admin' 


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    recruiter_level = models.CharField(max_length=50, choices=[('junior', 'Junior'), ('senior', 'Senior')])

class Company(models.Model):
    is_approved = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    #location = models.CharField(max_length=100)
# accounts/models.py

from django.db import models
from django.utils import timezone
from datetime import timedelta

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(minutes=10)
