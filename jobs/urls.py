from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='list'),
    path('jobs/<int:pk>/', views.job_detail, name='detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply'),
    path('jobs/<int:pk>/save/', views.toggle_save, name='save'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('saved/', views.saved_jobs, name='saved'),
    path('admin/jobs/', views.admin_jobs, name='admin_jobs'),
    path('admin/jobs/new/', views.admin_job_create, name='admin_job_create'),
    path('admin/jobs/<int:pk>/edit/', views.admin_job_edit, name='admin_job_edit'),
]
