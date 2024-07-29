# employer/filters.py
import django_filters
from .models import Job, JobApplication

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    is_remote = django_filters.BooleanFilter()
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte')
    application_deadline = django_filters.DateFilter(field_name='application_deadline', lookup_expr='gte')

    class Meta:
        model = Job
        fields = ['title', 'location', 'is_remote', 'salary_min', 'salary_max', 'application_deadline']

class JobApplicationFilter(django_filters.FilterSet):
    job = django_filters.NumberFilter(field_name='job', lookup_expr='exact')
    status = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = JobApplication
        fields = ['job', 'status']
