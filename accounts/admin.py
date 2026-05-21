from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'batch_year', 'experience_level', 'is_placement_admin')
    list_filter = ('branch', 'batch_year', 'is_placement_admin')
    search_fields = ('user__username', 'user__email', 'skills')
