from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet, basename='chatroom')

urlpatterns = [
    path('', include(router.urls)),
    path('chatrooms/<int:chat_room_pk>/messages/', MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='chat-messages'),
]