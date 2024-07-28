from rest_framework import serializers
from .models import Job, JobCategory, JobCategoryRelation

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

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'responsibilities', 'qualifications', 'nice_to_have', 'employment_type', 
                  'location', 'salary_min', 'salary_max', 'is_remote', 'application_deadline', 'posted_at', 'status', 
                  'views_count', 'applications_count', 'experience_level', 'job_function', 'categories']

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

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'resume_url', 'cover_letter', 'status', 'applied_at', 'updated_at', 'stage']
        read_only_fields = ['job_seeker', 'status', 'applied_at', 'updated_at']
