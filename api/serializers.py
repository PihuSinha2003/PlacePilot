from rest_framework import serializers

from jobs.models import Job


class JobSerializer(serializers.ModelSerializer):
    days_left = serializers.ReadOnlyField()
    is_deadline_near = serializers.ReadOnlyField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'job_type', 'role', 'location',
            'description', 'required_skills', 'min_batch_year', 'max_batch_year',
            'experience_level', 'salary', 'deadline', 'is_active', 'created_at',
            'days_left', 'is_deadline_near',
        ]
