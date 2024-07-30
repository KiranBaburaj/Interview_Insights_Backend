from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    jobseeker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='jobseeker_chats', on_delete=models.CASCADE)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='employer_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.jobseeker.username} and {self.employer.username}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"