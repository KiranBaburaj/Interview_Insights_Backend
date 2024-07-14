# employer/serializers.py

from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'logo_url', 'website_url', 'industry', 'company_size',
            'founded_date', 'description', 'headquarters_location',
            'employee_count', 'tech_stack','gst_document','is_approved'
        ]
