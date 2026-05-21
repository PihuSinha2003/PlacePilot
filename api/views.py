from django.utils import timezone
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from jobs.models import Job
from jobs.filters import JobFilter

from .serializers import JobSerializer


class JobListAPI(generics.ListAPIView):
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'company', 'role', 'required_skills']

    def get_queryset(self):
        return Job.objects.filter(
            is_active=True,
            deadline__gte=timezone.now().date(),
        )


class JobDetailAPI(generics.RetrieveAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.filter(is_active=True)
