from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Profile

from .filters import JobFilter
from .forms import JobForm
from .models import Application, Job, SavedJob


def home(request):
    recent_jobs = Job.objects.filter(is_active=True, deadline__gte=timezone.now().date())[:6]
    return render(request, 'jobs/home.html', {'recent_jobs': recent_jobs})


def job_list(request):
    jobs = Job.objects.filter(is_active=True, deadline__gte=timezone.now().date())
    job_filter = JobFilter(request.GET, queryset=jobs)
    jobs = job_filter.qs

    saved_ids = []
    applied_ids = []
    if request.user.is_authenticated:
        saved_ids = list(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))
        applied_ids = list(Application.objects.filter(user=request.user).values_list('job_id', flat=True))

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'filter': job_filter,
        'saved_ids': saved_ids,
        'applied_ids': applied_ids,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    saved = False
    applied = False
    if request.user.is_authenticated:
        saved = SavedJob.objects.filter(user=request.user, job=job).exists()
        applied = Application.objects.filter(user=request.user, job=job).exists()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'saved': saved,
        'applied': applied,
    })


@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    applications = Application.objects.filter(user=request.user).select_related('job')
    saved = SavedJob.objects.filter(user=request.user).select_related('job')
    upcoming = Application.objects.filter(
        user=request.user,
        job__deadline__gte=timezone.now().date(),
    ).select_related('job').order_by('job__deadline')[:5]

    recommended = _get_recommended_jobs(profile)

    context = {
        'applied_count': applications.count(),
        'saved_count': saved.count(),
        'shortlisted_count': applications.filter(status='shortlisted').count(),
        'recent_applications': applications[:5],
        'saved_jobs': saved[:5],
        'upcoming_deadlines': upcoming,
        'recommended_jobs': recommended[:6],
        'profile': profile,
    }
    return render(request, 'jobs/dashboard.html', context)


def _get_recommended_jobs(profile):
    jobs = Job.objects.filter(is_active=True, deadline__gte=timezone.now().date())
    jobs = jobs.filter(
        min_batch_year__lte=profile.batch_year,
        max_batch_year__gte=profile.batch_year,
    )

    user_skills = profile.skill_list()
    if user_skills:
        skill_query = Q()
        for skill in user_skills:
            skill_query |= Q(required_skills__icontains=skill)
        jobs = jobs.filter(skill_query)

    if profile.experience_level:
        jobs = jobs.filter(experience_level=profile.experience_level)

    applied_ids = Application.objects.filter(user=profile.user).values_list('job_id', flat=True)
    return jobs.exclude(id__in=applied_ids)[:12]


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    if job.deadline < timezone.now().date():
        messages.error(request, 'This opportunity has closed.')
        return redirect('jobs:detail', pk=pk)

    cover_note = request.POST.get('cover_note', '')
    _, created = Application.objects.get_or_create(
        user=request.user,
        job=job,
        defaults={'cover_note': cover_note},
    )
    if created:
        messages.success(request, f'Applied to {job.title}.')
    else:
        messages.info(request, 'You already applied for this role.')

    SavedJob.objects.filter(user=request.user, job=job).delete()
    return redirect('jobs:detail', pk=pk)


@login_required
def toggle_save(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        saved.delete()
        messages.info(request, 'Removed from saved jobs.')
    else:
        messages.success(request, 'Job saved for later.')

    next_url = request.GET.get('next', 'jobs:list')
    if next_url.startswith('/'):
        return redirect(next_url)
    return redirect(next_url)


@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def saved_jobs(request):
    saved = SavedJob.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': saved})


def _is_placement_admin(user):
    if user.is_superuser:
        return True
    profile = getattr(user, 'profile', None)
    return profile and profile.is_placement_admin


@login_required
def admin_jobs(request):
    if not _is_placement_admin(request.user):
        messages.error(request, 'Placement admin access required.')
        return redirect('jobs:dashboard')

    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'jobs/admin_jobs.html', {'jobs': jobs})


@login_required
def admin_job_create(request):
    if not _is_placement_admin(request.user):
        messages.error(request, 'Placement admin access required.')
        return redirect('jobs:dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Opportunity posted.')
            return redirect('jobs:admin_jobs')
    else:
        form = JobForm()

    return render(request, 'jobs/admin_job_form.html', {'form': form, 'title': 'Post Opportunity'})


@login_required
def admin_job_edit(request, pk):
    if not _is_placement_admin(request.user):
        messages.error(request, 'Placement admin access required.')
        return redirect('jobs:dashboard')

    job = get_object_or_404(Job, pk=pk, posted_by=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity updated.')
            return redirect('jobs:admin_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/admin_job_form.html', {'form': form, 'title': 'Edit Opportunity'})
