# urls.py
from django.urls import path
from .views import ScheduleInterviewView, UpdateInterviewScheduleView, ListInterviewSchedulesView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScheduleInterviewView,
    UpdateInterviewScheduleView,
    ListInterviewSchedulesView,

    InterviewFeedbackViewSet
)

router = DefaultRouter()
router.register(r'interview-feedbacks', InterviewFeedbackViewSet, basename='interviewfeedback')


urlpatterns = [
    # ... other URL patterns ...
     path('', include(router.urls)),  
    path('schedule-interview/', ScheduleInterviewView.as_view(), name='schedule_interview'),
    path('update-interview/<int:pk>/', UpdateInterviewScheduleView.as_view(), name='update_interview'),
    path('interview-schedules/', ListInterviewSchedulesView.as_view(), name='list_interviews'),
]