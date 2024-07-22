from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, JobSeekerViewSet, EmployerViewSet, RecruiterViewSet, CompanyViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobseekers', JobSeekerViewSet)
router.register(r'employers', EmployerViewSet)
router.register(r'recruiters', RecruiterViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
