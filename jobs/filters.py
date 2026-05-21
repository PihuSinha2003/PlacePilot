import django_filters
from django.db.models import Q

from .models import Job


class JobFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='search', label='Search')
    role = django_filters.CharFilter(field_name='role', lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    batch_year = django_filters.NumberFilter(method='filter_batch')
    job_type = django_filters.ChoiceFilter(choices=Job.TYPE_CHOICES)

    class Meta:
        model = Job
        fields = ['role', 'location', 'job_type', 'experience_level']

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
            | Q(company__icontains=value)
            | Q(description__icontains=value)
            | Q(required_skills__icontains=value)
        )

    def filter_batch(self, queryset, name, value):
        return queryset.filter(min_batch_year__lte=value, max_batch_year__gte=value)
