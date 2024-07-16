from rest_framework import serializers
from .models import Job, JobCategory, JobCategoryRelation

class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ['id', 'name']

class JobSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=JobCategory.objects.all(), many=True)

    class Meta:
        model = Job
        fields = [
            'id', 'employer', 'title', 'description', 'responsibilities', 
            'qualifications', 'nice_to_have', 'employment_type', 'location', 
            'salary_min', 'salary_max', 'is_remote', 'application_deadline', 
            'posted_at', 'status', 'views_count', 'applications_count', 
            'experience_level', 'job_function', 'categories'
        ]

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        job = Job.objects.create(**validated_data)
        job.categories.set(categories_data)
        return job

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', None)
        instance = super().update(instance, validated_data)

        if categories_data is not None:
            instance.categories.set(categories_data)
        
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = JobCategorySerializer(instance.categories.all(), many=True).data
        return representation
