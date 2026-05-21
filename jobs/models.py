from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Job(models.Model):
    TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ]
    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('0-1', '0-1 years'),
        ('1-2', '1-2 years'),
        ('2+', '2+ years'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='full_time')
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.TextField(blank=True)
    min_batch_year = models.PositiveIntegerField(default=2024)
    max_batch_year = models.PositiveIntegerField(default=2027)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='fresher')
    salary = models.CharField(max_length=80, blank=True)
    deadline = models.DateField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} at {self.company}'

    @property
    def days_left(self):
        delta = (self.deadline - timezone.now().date()).days
        return delta

    @property
    def is_deadline_near(self):
        return 0 <= self.days_left <= 7

    def skill_list(self):
        if not self.required_skills:
            return []
        return [s.strip().lower() for s in self.required_skills.split(',') if s.strip()]


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_note = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f'{self.user.username} -> {self.job.title}'


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f'{self.user.username} saved {self.job.title}'
