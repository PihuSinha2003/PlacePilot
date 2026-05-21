from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from accounts.models import Profile
from jobs.models import Job
from notices.models import InterviewSchedule, Notice


class Command(BaseCommand):
    help = 'Load sample data for demo and development'

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username='placement',
            defaults={
                'email': 'placement@college.edu',
                'first_name': 'Placement',
                'last_name': 'Cell',
            },
        )
        if created:
            admin.set_password('placement123')
            admin.save()

        profile, _ = Profile.objects.get_or_create(user=admin)
        profile.is_placement_admin = True
        profile.branch = 'CSE'
        profile.batch_year = 2020
        profile.save()

        student, created = User.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@college.edu',
                'first_name': 'Rahul',
                'last_name': 'Sharma',
            },
        )
        if created:
            student.set_password('student123')
            student.save()

        sprofile, _ = Profile.objects.get_or_create(user=student)
        sprofile.branch = 'CSE'
        sprofile.batch_year = 2026
        sprofile.skills = 'Python, Django, SQL, Git'
        sprofile.experience_level = 'fresher'
        sprofile.save()

        today = timezone.now().date()
        jobs_data = [
            {
                'title': 'Software Engineer Intern',
                'company': 'TechNova Solutions',
                'job_type': 'internship',
                'role': 'Backend Developer',
                'location': 'Bangalore',
                'description': 'Work on Django REST APIs and internal tools. Mentorship from senior engineers included.',
                'required_skills': 'Python, Django, SQL',
                'salary': '₹25,000/month',
                'deadline': today + timedelta(days=14),
            },
            {
                'title': 'Graduate Trainee',
                'company': 'Infosys',
                'job_type': 'full_time',
                'role': 'Software Developer',
                'location': 'Hyderabad',
                'description': 'Campus hiring for 2026 batch. Training program followed by project deployment.',
                'required_skills': 'Java, Python, Communication',
                'salary': '4.5 LPA',
                'deadline': today + timedelta(days=21),
            },
            {
                'title': 'Frontend Intern',
                'company': 'PixelCraft',
                'job_type': 'internship',
                'role': 'UI Developer',
                'location': 'Remote',
                'description': 'Build responsive dashboards using React and Bootstrap. 3-month internship.',
                'required_skills': 'JavaScript, React, HTML, CSS',
                'salary': '₹15,000/month',
                'deadline': today + timedelta(days=5),
            },
            {
                'title': 'Data Analyst',
                'company': 'AnalyticsPro',
                'job_type': 'full_time',
                'role': 'Data Analyst',
                'location': 'Pune',
                'description': 'Analyze campus placement trends and build reports using Python and SQL.',
                'required_skills': 'Python, SQL, Excel',
                'salary': '6 LPA',
                'deadline': today + timedelta(days=30),
            },
        ]

        for data in jobs_data:
            Job.objects.get_or_create(
                title=data['title'],
                company=data['company'],
                defaults={**data, 'posted_by': admin, 'min_batch_year': 2025, 'max_batch_year': 2027},
            )

        Notice.objects.get_or_create(
            title='Campus Drive Registration Open',
            defaults={
                'content': 'All final-year students must register on the portal before applying to on-campus drives. Carry updated resume and ID card for interviews.',
                'posted_by': admin,
                'is_pinned': True,
            },
        )

        job = Job.objects.first()
        if job:
            InterviewSchedule.objects.get_or_create(
                title='TechNova Internship Round 1',
                company='TechNova Solutions',
                defaults={
                    'job': job,
                    'scheduled_date': today + timedelta(days=10),
                    'scheduled_time': '10:00',
                    'venue': 'Seminar Hall A, Block 3',
                    'notes': 'Bring laptop and college ID. Aptitude test followed by technical interview.',
                    'posted_by': admin,
                },
            )

        self.stdout.write(self.style.SUCCESS('Sample data loaded.'))
        self.stdout.write('  Admin: placement / placement123')
        self.stdout.write('  Student: student / student123')
