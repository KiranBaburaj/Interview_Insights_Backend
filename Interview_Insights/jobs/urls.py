from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckApplicationStatusView, JobApplicationViewSet, JobViewSet, JobCategoryViewSet
from .views import  UpdateApplicationStatusView
from .views import job_applicants,JobApplicationList


router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'job-categories', JobCategoryViewSet)
router.register(r'applications', JobApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
     path('jobs/<int:job_id>/applicants/', job_applicants, name='job-applicants'),
      path('myapplications/', JobApplicationList.as_view(), name='job-application-list'),
       path('jobs/<int:job_id>/check-application-status/', CheckApplicationStatusView.as_view(), name='check-application-status'),
    path('jobs/<int:job_id>/applications/status/', UpdateApplicationStatusView.as_view(), name='check-application-status'),]
