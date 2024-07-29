# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobSeekerViewSet

router = DefaultRouter()
router.register(r'profile', JobSeekerViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
