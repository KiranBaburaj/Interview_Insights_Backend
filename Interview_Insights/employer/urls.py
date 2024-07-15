# employer/urls.py

from django.urls import path
from .views import CompanyListCreateView, CompanyDetailView
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)



urlpatterns = [
     path('', include(router.urls)),
    path('companies/', CompanyListCreateView.as_view(), name='company_list_create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
]
