from rest_framework import serializers
from .models import Job, JobCategory, JobCategoryRelation
from employer.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']  # Add other fields if necessary

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name']

class JobCategoryRelationSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=JobCategory.objects.all()
    )

    class Meta:
        model = JobCategoryRelation
        fields = ['category']

class JobSerializer(serializers.ModelSerializer):
    categories = JobCategoryRelationSerializer(source='jobcategoryrelation_set', many=True)
    company = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'responsibilities', 'qualifications', 'nice_to_have', 'employment_type', 
                  'location', 'salary_min', 'salary_max', 'is_remote', 'application_deadline', 'posted_at', 'status', 
                  'views_count', 'applications_count', 'experience_level', 'job_function', 'categories','company','employer']

    def get_company(self, job):
        # Navigate through the Employer to get the Company details
        employer = job.employer
        company = employer.company if employer else None
        return CompanySerializer(company).data if company else None
    
    def create(self, validated_data):
        categories_data = validated_data.pop('jobcategoryrelation_set')
        job = Job.objects.create(**validated_data)
        for category_data in categories_data:
            category_name = category_data['category']
            category, created = JobCategory.objects.get_or_create(name=category_name)
            JobCategoryRelation.objects.create(job=job, category=category)
        return job

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('jobcategoryrelation_set')
        instance = super().update(instance, validated_data)
        
        instance.jobcategoryrelation_set.all().delete()
        for category_data in categories_data:
            category_name = category_data['category']
            category, created = JobCategory.objects.get_or_create(name=category_name)
            JobCategoryRelation.objects.create(job=instance, category=category)
        return instance


# serializers.py
from rest_framework import serializers
from .models import JobApplication
from users.serializers import JobSeekerSerializer

class JobApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True) 
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())  # Ensure this is the correct field type
    job_seeker = JobSeekerSerializer(read_only=True)
    company = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'job_seeker', 'resume_url', 'cover_letter', 'status', 'applied_at', 'updated_at', 'stage','company','job_details']
        read_only_fields = ['job_seeker', 'status', 'applied_at', 'updated_at','job_details']

    def get_company(self, obj):
        # Navigate through the job to the employer to get the company details
        job = obj.job
        employer = job.employer if job else None
        company = employer.company if employer else None
        return CompanySerializer(company).data if company else None

class JobApplicationStatusSerializer(serializers.Serializer):
    hasApplied = serializers.BooleanField()