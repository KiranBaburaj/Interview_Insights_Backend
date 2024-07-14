# employer/urls.py

from django.urls import path
from .views import CompanyListCreateView, CompanyDetailView

urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company_list_create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
]
