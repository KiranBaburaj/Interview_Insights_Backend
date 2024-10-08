from rest_framework import serializers
from .models import Job, JobCategory, JobCategoryRelation, JobSkill, SavedJob
from employer.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']  # Add other fields if necessary

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name']

class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = ['id', 'name', 'description']

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
    skills_required = JobSkillSerializer(many=True, required=False)  # Add this for handling required skills

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'responsibilities', 'qualifications', 'nice_to_have', 'employment_type', 
                  'location', 'salary_min', 'salary_max', 'is_remote', 'application_deadline', 'posted_at', 'status', 
                  'views_count', 'applications_count', 'experience_level', 'job_function', 'categories', 'company', 
                  'employer', 'skills_required']

    def get_company(self, job):
        # Navigate through the Employer to get the Company details
        employer = job.employer
        company = employer.company if employer else None
        return CompanySerializer(company).data if company else None

    def create(self, validated_data):
        # Handle categories
        categories_data = validated_data.pop('jobcategoryrelation_set', [])
        
        # Handle skills
        skills_data = validated_data.pop('skills_required', [])
        
        # Create the job instance without Many-to-Many fields
        job = Job.objects.create(**validated_data)
        
        # Create job categories
        for category_data in categories_data:
            category_name = category_data['category']
            category, created = JobCategory.objects.get_or_create(name=category_name)
            JobCategoryRelation.objects.create(job=job, category=category)

        # Create job skills
        for skill_data in skills_data:
            skill_name = skill_data['name']  # Ensure this is the correct field for the skill name
            skill, created = JobSkill.objects.get_or_create(name=skill_name)
            job.skills_required.add(skill)  # Add skill to the job's Many-to-Many relationship

        return job

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('jobcategoryrelation_set', [])
        skills_data = validated_data.pop('skills_required', [])
        
        instance = super().update(instance, validated_data)
        
        # Update categories
        instance.jobcategoryrelation_set.all().delete()
        for category_data in categories_data:
            category_name = category_data['category']
            category, created = JobCategory.objects.get_or_create(name=category_name)
            JobCategoryRelation.objects.create(job=instance, category=category)

        # Update skills
        instance.skills_required.clear()
        for skill_data in skills_data:
            skill_name = skill_data['name']  # Ensure this is the correct field for the skill name
            skill, created = JobSkill.objects.get_or_create(name=skill_name)
            instance.skills_required.add(skill)

        return instance
# serializers.py
from rest_framework import serializers
from .models import JobApplication
from jobseeker.serializers import JobSeekerSerializer

class JobApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True) 
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())  # Ensure this is the correct field type
    job_seeker = JobSeekerSerializer(read_only=True)
    company = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'job_seeker', 'resume', 'cover_letter', 'status', 'applied_at', 'updated_at', 'stage','company','job_details']
        read_only_fields = ['job_seeker', 'status', 'applied_at', 'updated_at','job_details']

    def get_company(self, obj):
        # Navigate through the job to the employer to get the company details
        job = obj.job
        employer = job.employer if job else None
        company = employer.company if employer else None
        return CompanySerializer(company).data if company else None
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
from rest_framework import serializers
from .models import JobApplication

class JobApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']

class SavedJobSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SavedJob
        fields = ['id', 'job_seeker', 'job', 'saved_at']
        read_only_fields = ['job_seeker', 'saved_at']