import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from .serializers import MessageSerializer

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            if message_type == 'chat_message':
                message = text_data_json.get('message')
                if message:
                    user = self.scope.get("user")
                    if user and user.is_authenticated:
                        # Save the message to the database
                        saved_message = await self.save_message(user, message)

                        # Send message to room group
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'chat_message',
                                'message': MessageSerializer(saved_message).data
                            }
                        )
                    else:
                        await self.send(text_data=json.dumps({
                            'error': 'Authentication required'
                        }))
                else:
                    await self.send(text_data=json.dumps({
                        'error': 'Message content is required'
                    }))
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Invalid message type'
                }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, user, message):
        chat_room = ChatRoom.objects.get(id=self.room_name)
        return Message.objects.create(
            chat_room=chat_room,
            sender=user,
            content=message
        )