from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication'),
        ('EEE', 'Electrical & Electronics'),
        ('ME', 'Mechanical'),
        ('CE', 'Civil'),
        ('Other', 'Other'),
    ]
    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('0-1', '0-1 years'),
        ('1-2', '1-2 years'),
        ('2+', '2+ years'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='CSE')
    batch_year = models.PositiveIntegerField(default=2026)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='fresher')
    phone = models.CharField(max_length=15, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    is_placement_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username}'

    def skill_list(self):
        if not self.skills:
            return []
        return [s.strip().lower() for s in self.skills.split(',') if s.strip()]
