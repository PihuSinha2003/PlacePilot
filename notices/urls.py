from django.urls import path

from . import views

app_name = 'notices'

urlpatterns = [
    path('', views.notice_list, name='list'),
    path('admin/', views.admin_notices, name='admin'),
    path('admin/notice/new/', views.admin_notice_create, name='notice_create'),
    path('admin/interview/new/', views.admin_interview_create, name='interview_create'),
]
