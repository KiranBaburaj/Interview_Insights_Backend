from django.shortcuts import render
from users.models import User 
# Create your views here.
from rest_framework import viewsets, permissions
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from rest_framework import viewsets, permissions, serializers

class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(jobseeker=user) | ChatRoom.objects.filter(employer=user)
    
    def perform_create(self, serializer):
        print (self.request.data)
        jobseeker = self.request.data.get('jobseeker_id')
        employer = self.request.data.get('employer_id')


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

# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        try:
            notification = self.get_object()
            notification.is_read = True
            notification.save()
            serializer = self.get_serializer(notification)
            return Response(serializer.data)
        except Notification.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
