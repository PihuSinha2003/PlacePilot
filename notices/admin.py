from django.contrib import admin

from .models import InterviewSchedule, Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_pinned', 'posted_by', 'created_at')
    list_filter = ('is_pinned',)


@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'scheduled_date', 'scheduled_time', 'venue')
    list_filter = ('scheduled_date',)
