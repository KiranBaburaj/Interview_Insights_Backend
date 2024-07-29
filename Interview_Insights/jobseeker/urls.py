from django.urls import path
from .views import JobSeekerRetrieveUpdateAPIView, JobSeekerListCreateAPIView, JobSeekerDetailAPIView

urlpatterns = [
    path('profile/', JobSeekerRetrieveUpdateAPIView.as_view(), name='jobseeker-profile'),
    path('jobseekers/', JobSeekerListCreateAPIView.as_view(), name='jobseeker-list'),
    path('jobseekers/<int:pk>/', JobSeekerDetailAPIView.as_view(), name='jobseeker-detail'),
]