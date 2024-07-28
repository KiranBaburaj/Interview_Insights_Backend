from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, JobViewSet, JobCategoryViewSet
from .views import  CheckApplicationStatusView

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'job-categories', JobCategoryViewSet)
router.register(r'applications', JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('jobs/<int:job_id>/applications/status/', CheckApplicationStatusView.as_view(), name='check-application-status'),]
