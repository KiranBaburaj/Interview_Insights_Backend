from django.shortcuts import render
from users.models import User 
# Create your views here.
from rest_framework import viewsets, permissions
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(jobseeker=user) | ChatRoom.objects.filter(employer=user)
    
    def perform_create(self, serializer):
        print (serializer)
        jobseeker = self.request.data.get('jobseekerId')
        employer = self.request.data.get('employerId')


        if not jobseeker or not employer:
            raise serializers.ValidationError("Both jobseekerId and employerId are required.")

        try:
            jobseeker_user = User.objects.get(id=jobseeker)
            employer_user = User.objects.get(id=employer)
        except User.DoesNotExist:
            raise serializers.ValidationError("Jobseeker or Employer not found.")

        serializer.save(jobseeker=jobseeker_user, employer=employer_user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(chat_room_id=self.kwargs['chat_room_pk'])

    def perform_create(self, serializer):
        chat_room = ChatRoom.objects.get(id=self.kwargs['chat_room_pk'])
        serializer.save(sender=self.request.user, chat_room=chat_room)