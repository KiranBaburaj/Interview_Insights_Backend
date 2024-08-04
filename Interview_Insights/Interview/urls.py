# urls.py
from django.urls import path
from .views import ScheduleInterviewView, UpdateInterviewScheduleView, ListInterviewSchedulesView

urlpatterns = [
    # ... other URL patterns ...
    path('schedule-interview/', ScheduleInterviewView.as_view(), name='schedule_interview'),
    path('update-interview/<int:pk>/', UpdateInterviewScheduleView.as_view(), name='update_interview'),
    path('interview-schedules/', ListInterviewSchedulesView.as_view(), name='list_interviews'),
]