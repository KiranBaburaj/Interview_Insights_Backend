# serializers.py
from rest_framework import serializers
from .models import InterviewSchedule
from rest_framework import serializers
from .models import InterviewFeedback

class InterviewScheduleSerializer(serializers.ModelSerializer):
    job_seeker_name = serializers.SerializerMethodField()
    class Meta:
        model = InterviewSchedule
        fields = ['id', 'job_application', 'scheduled_time', 'duration', 'location', 'notes', 'is_confirmed','job_seeker_name']

    def get_job_seeker_name(self, obj):
        return obj.job_application.job_seeker.user.full_name


class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = '__all__'
