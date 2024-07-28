from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobApplicationViewSet, JobViewSet, JobCategoryViewSet


router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'job-categories', JobCategoryViewSet)
router.register(r'applications', JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
