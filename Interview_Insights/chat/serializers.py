from rest_framework import serializers
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

class ChatRoomSerializer(serializers.ModelSerializer):
    jobseeker = UserSerializer(read_only=True)
    employer = UserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'jobseeker', 'employer', 'created_at', 'last_message']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    def create(self, validated_data):
        print("validated_data",validated_data)
        # Ensure that jobseeker and employer are properly set
        jobseeker = validated_data.get('jobseeker')
        employer = validated_data.get('employer')

        if jobseeker is None or employer is None:
            raise serializers.ValidationError("Both jobseeker and employer must be provided.")

        return super().create(validated_data)