from django.urls import path

from .views import JobDetailAPI, JobListAPI

app_name = 'api'

urlpatterns = [
    path('jobs/', JobListAPI.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobDetailAPI.as_view(), name='job_detail'),
]
