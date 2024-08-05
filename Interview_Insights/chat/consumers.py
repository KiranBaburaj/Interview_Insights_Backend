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
        notification = await self.create_notifications(user_id, f"New message from {full_name}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id,
                'full_name': full_name,
                'notification_id': notification.id  # Include the notification ID
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        full_name = event['full_name']
        notification_id = event['notification_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
            'full_name': full_name,
            'notification_id': notification_id  # Include the notification ID
        }))

    @database_sync_to_async
    def save_message(self, user_id, message):
        user = User.objects.get(id=user_id)
        chat_room = ChatRoom.objects.get(id=self.room_id)
        Message.objects.create(chat_room=chat_room, sender=user, content=message)

    @database_sync_to_async
    def create_notifications(self, sender_id, message):
        sender = User.objects.get(id=sender_id)
        chat_room = ChatRoom.objects.get(id=self.room_id)
        recipients = [chat_room.jobseeker, chat_room.employer]
        notification = None
        
        for user in recipients:
            if user.id != int(sender_id):
                notification = Notification.objects.create(
                    user=user,
                    message=message,
                    notification_type='CHAT'
                )
        return notification

# consumers.py

# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

logger = logging.getLogger('notifications')

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = f"user_{self.user.id}"
        self.room_group_name = f'notifications_{self.user.id}'

        logger.info(f"Connecting to room: {self.room_group_name} for user: {self.user.id}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.info(f"WebSocket connection accepted for user: {self.user.id}")

    async def disconnect(self, close_code):
        logger.info(f"Disconnecting from room: {self.room_group_name} for user: {self.user.id}")

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        logger.info(f"WebSocket connection closed for user: {self.user.id}")

    async def receive(self, text_data):
        logger.info(f"Received data: {text_data} from user: {self.user.id}")
        data = json.loads(text_data)
        notification_id = data.get('notification_id')

        if notification_id:
            try:
                notification = await database_sync_to_async(Notification.objects.get)(id=notification_id)
                if notification:
                    notification.is_read = True
                    notification.save()
                    logger.info(f"Notification ID {notification_id} marked as read for user: {self.user.id}")

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'notification_update',
                            'notification': {
                                'id': notification.id,
                                'message': notification.message,
                                'notification_type': notification.notification_type,
                                'is_read': notification.is_read,
                                'created_at': notification.created_at.isoformat()
                            }
                        }
                    )
            except Notification.DoesNotExist:
                logger.warning(f"Notification ID {notification_id} does not exist for user: {self.user.id}")
            except Exception as e:
                logger.error(f"Error while processing notification ID {notification_id} for user: {self.user.id} - {e}")

    async def notification_update(self, event):
        notification = event['notification']
        logger.debug(f"Sending notification update: {notification} to user: {self.user.id}")

        await self.send(text_data=json.dumps({
            'notification': notification
        }))
