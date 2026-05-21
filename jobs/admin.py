from django.contrib import admin

from .models import Application, Job, SavedJob


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'location', 'deadline', 'is_active')
    list_filter = ('job_type', 'location', 'experience_level', 'is_active')
    search_fields = ('title', 'company', 'role', 'required_skills')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'job__title')


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
