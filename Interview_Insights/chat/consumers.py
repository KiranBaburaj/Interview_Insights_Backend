# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import ChatRoom, Message, Notification
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger('chat')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        full_name = text_data_json['full_name']

        await self.save_message(user_id, message)

        # Create a notification for the chat message
       

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'full_name': full_name,
                
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        full_name = event['full_name']
        

        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'full_name': full_name,
            
        }))

    @database_sync_to_async
    def save_message(self, user_id, message):
        user = User.objects.get(id=user_id)
        chat_room = ChatRoom.objects.get(id=self.room_id)
        Message.objects.create(chat_room=chat_room, sender=user, content=message)

# consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Notification, ChatRoom

User = get_user_model()
logger = logging.getLogger('notifications')
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'notifications_{self.user_id}'
        logger.info(f"WebSocket name user: {self.room_group_name}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"WebSocket connection accepted for user: {self.user_id}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket connection closed for user: {self.user_id}")

    async def receive(self, text_data):
        logger.info(f"Received data: {text_data}")
        data = json.loads(text_data)
        user_id = data.get('user_id')
        message = data.get('message')
        room_id = data.get('room_id')

        # Create a notification for the message
        notification_recipients = await self.create_notification(user_id, message, room_id)

        for recipient_id, notification in notification_recipients:
            await self.channel_layer.group_send(
                f'notifications_{recipient_id}',
                {
                    'type': 'notification_message',
                    'message': message,
                    'user_id': user_id,
                    'room_id': room_id,
                    'notification': {
                        'id': notification.id,
                        'message': notification.message,
                        'is_read':notification.is_read,
                        'user_id': recipient_id,
                        'notification_type': notification.notification_type,
                        'timestamp': notification.created_at.isoformat(),
                    }
                }
            )
            logger.info(f"notifications_{recipient_id}")

    async def notification_message(self, event):
        message = event['message']
        user_id = event['user_id']
        room_id = event['room_id']

        notification = event['notification']
        logger.info(f"message : {message}")

        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'room_id': room_id,

            'notification': notification
        }))

    @database_sync_to_async
    def create_notification(self, user_id, message, room_id):
        sender = User.objects.get(id=user_id)
        chat_room = ChatRoom.objects.get(id=room_id)
        recipients = [chat_room.jobseeker, chat_room.employer]

        notification_recipients = []
        for user in recipients:
            if user.id != int(user_id):
                notification = Notification.objects.create(
                    user=user,
                    message=message,
                    notification_type='CHAT'
                )
                notification_recipients.append((user.id, notification))
        
        return notification_recipients
