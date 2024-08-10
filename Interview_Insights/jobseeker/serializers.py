from rest_framework import serializers
from users.models import JobSeeker, User
  
from rest_framework import serializers
from .models import Education, WorkExperience, Skill
from users.models import JobSeeker, User

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
        fields = ['email', 'full_name']
class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    educations = EducationSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    work_experience = WorkExperienceSerializer(many=True, required=False)

    class Meta:
        model = JobSeeker
        fields = '__all__'
    def to_internal_value(self, data):
        print("Data before validation:", data)
        return super().to_internal_value(data)

    def create(self, validated_data):
        print("Creating JobSeeker with validated data:", validated_data)
        
        educations_data = validated_data.pop('educations', [])
        skills_data = validated_data.pop('skills', [])
        work_experience_data = validated_data.pop('work_experience', [])
        
        print("Educations data:", educations_data)
        print("Skills data:", skills_data)
        print("Work experience data:", work_experience_data)
        
        job_seeker = JobSeeker.objects.create(**validated_data)
        
        for education_data in educations_data:
            print("Creating Education with data:", education_data)
            Education.objects.create(job_seeker=job_seeker, **education_data)

        for skill_data in skills_data:
            print("Creating Skill with data:", skill_data)
            Skill.objects.create(job_seeker=job_seeker, **skill_data)

        for work_experience_data in work_experience_data:
            print("Creating WorkExperience with data:", work_experience_data)
            WorkExperience.objects.create(job_seeker=job_seeker, **work_experience_data)

        return job_seeker

    def update(self, instance, validated_data):
        print("Updating JobSeeker with validated data:", validated_data)
        validated_data['job_seeker'] = self.context['request'].user.jobseeker
        educations_data = validated_data.pop('educations', [])
        skills_data = validated_data.pop('skills', [])
        work_experience_data = validated_data.pop('work_experience', [])
        
        print("Educations data:", educations_data)
        print("Skills data:", skills_data)
        print("Work experience data:", work_experience_data)
        
        # Update the JobSeeker instance
        instance = super().update(instance, validated_data)
        print("Updated JobSeeker instance:", instance)

        # Update or create educations
        for education_data in educations_data:
            print("Updating or creating Education with data:", education_data)
            Education.objects.update_or_create(
                job_seeker=instance,
                field_of_study=education_data.get('field_of_study'),
                defaults=education_data
            )

        # Update or create skills
        for skill_data in skills_data:
            print("Updating or creating Skill with data:", skill_data)
            Skill.objects.update_or_create(
                job_seeker=instance,
                skill_name=skill_data.get('skill_name'),
                defaults=skill_data
            )

        # Update or create work experiences
        for work_experience_data in work_experience_data:
            print("Updating or creating WorkExperience with data:", work_experience_data)
            WorkExperience.objects.update_or_create(
                job_seeker=instance,
                job_title=work_experience_data.get('job_title'),
                defaults=work_experience_data
            )

        instance.refresh_from_db()
        
        # Re-fetch related fields
        instance.education_set.set(Education.objects.filter(job_seeker=instance))
        instance.skill_set.set(Skill.objects.filter(job_seeker=instance))
        instance.workexperience_set.set(WorkExperience.objects.filter(job_seeker=instance))

        return instance