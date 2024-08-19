from django.shortcuts import render
from .models import ChatRoom, Message,Notification
from .serializers import ChatRoomSerializer, MessageSerializer,NotificationSerializer
from rest_framework import viewsets, permissions, serializers,status
from rest_framework.response import Response
from users.models import User
from rest_framework.decorators import action



class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(jobseeker=user) | ChatRoom.objects.filter(employer=user)
    
    def perform_create(self, serializer):
        jobseeker_id = self.request.data.get('jobseeker_id')
        employer_id = self.request.data.get('employer_id')

        if not jobseeker_id or not employer_id:
            raise serializers.ValidationError("Both jobseeker_id and employer_id are required.")

        try:
            jobseeker_user = User.objects.get(id=jobseeker_id)
            employer_user = User.objects.get(id=employer_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Jobseeker or Employer not found.")

        # Use get_or_create to avoid duplication
        chat_room, created = ChatRoom.objects.get_or_create(
            jobseeker=jobseeker_user,
            employer=employer_user
        )

        # Use serializer to validate and update the instance
        serializer.instance = chat_room
        return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        jobseeker_id = request.data.get('jobseeker_id')
        employer_id = request.data.get('employer_id')

        if not jobseeker_id or not employer_id:
            return Response(
                {"detail": "Both jobseeker_id and employer_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            jobseeker_user = User.objects.get(id=jobseeker_id)
            employer_user = User.objects.get(id=employer_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "Jobseeker or Employer not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use get_or_create to avoid duplication
        chat_room, created = ChatRoom.objects.get_or_create(
            jobseeker=jobseeker_user,
            employer=employer_user
        )

        serializer = self.get_serializer(chat_room)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(chat_room_id=self.kwargs['chat_room_pk'])

    def perform_create(self, serializer):
        chat_room = ChatRoom.objects.get(id=self.kwargs['chat_room_pk'])
        serializer.save(sender=self.request.user, chat_room=chat_room)

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
