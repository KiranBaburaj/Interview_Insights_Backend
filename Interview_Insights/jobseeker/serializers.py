from rest_framework import serializers
from users.models import JobSeeker, User
  
from rest_framework import serializers
from .models import Education, WorkExperience, Skill
from users.models import JobSeeker, User
from Interview.models import InterviewFeedback, InterviewSchedule
from Interview.serializers import InterviewFeedbackSerializer, InterviewScheduleSerializer
from jobs.models import  JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = JobApplication
        fields = '__all__'



class EducationSerializer(serializers.ModelSerializer):
    job_seeker = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Education
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
    job_seeker = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WorkExperience
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    job_seeker = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Skill
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name','id']
class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    educations = EducationSerializer(many=True ,required=False)
    skills = SkillSerializer(many=True,required=False)
    work_experience = WorkExperienceSerializer(many=True,required=False)
    interview_feedback = serializers.SerializerMethodField()
    myapplications = serializers.SerializerMethodField()
    interview_schedule = serializers.SerializerMethodField()


    class Meta:
        model = JobSeeker
        fields = [
            'user', 'phone_number', 'date_of_birth', 'profile_photo', 'bio', 'interview_schedule','myapplications',
            'linkedin_url', 'portfolio_url', 'resume', 'current_job_title', 
            'job_preferences', 'educations', 'skills', 'work_experience','interview_feedback','visible_applications'
        ]
    def get_interview_feedback(self, obj):
        feedbacks = InterviewFeedback.objects.filter(
            interview_schedule__job_application__job_seeker=obj
        )
        return InterviewFeedbackSerializer(feedbacks, many=True).data
    
    def get_interview_schedule(self, obj):
        schedule = InterviewSchedule.objects.filter(
            job_application__job_seeker=obj
        )
        return InterviewScheduleSerializer(schedule, many=True).data
    
    
    def get_myapplications(self, obj):
        applications = JobApplication.objects.filter(
            job_seeker=obj
        )
        return JobApplicationSerializer(applications, many=True).data
    
    def update(self, instance, validated_data):
        educations_data = validated_data.pop('educations', [])
        skills_data = validated_data.pop('skills', [])
        work_experience_data = validated_data.pop('work_experience', [])
        
        # Update the JobSeeker instance fields
        instance = super().update(instance, validated_data)

        # Handle Education records
        new_education_ids = set(education.get('id') for education in educations_data if education.get('id'))
        instance.educations.exclude(id__in=new_education_ids).delete()
        for education_data in educations_data:
            Education.objects.update_or_create(
                job_seeker=instance,
                id=education_data.get('id'),
                defaults=education_data
            )

        # Handle Skill records
        new_skill_ids = set(skill.get('id') for skill in skills_data if skill.get('id'))
        instance.skills.exclude(id__in=new_skill_ids).delete()
        for skill_data in skills_data:
            Skill.objects.update_or_create(
                job_seeker=instance,
                id=skill_data.get('id'),
                defaults=skill_data
            )

        # Handle WorkExperience records
        new_work_experience_ids = set(work_exp.get('id') for work_exp in work_experience_data if work_exp.get('id'))
        instance.work_experience.exclude(id__in=new_work_experience_ids).delete()
        for work_experience_data in work_experience_data:
            WorkExperience.objects.update_or_create(
                job_seeker=instance,
                id=work_experience_data.get('id'),
                defaults=work_experience_data
            )

        return instance
