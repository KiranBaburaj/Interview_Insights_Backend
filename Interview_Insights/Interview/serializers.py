# serializers.py
from rest_framework import serializers
from .models import InterviewSchedule

class InterviewScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSchedule
        fields = ['id', 'job_application', 'scheduled_time', 'duration', 'location', 'notes', 'is_confirmed']