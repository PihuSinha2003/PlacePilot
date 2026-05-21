from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import Profile

from .forms import InterviewForm, NoticeForm
from .models import InterviewSchedule, Notice


def notice_list(request):
    notices = Notice.objects.all()[:20]
    interviews = InterviewSchedule.objects.filter(
        scheduled_date__gte=timezone.now().date()
    )[:10]
    return render(request, 'notices/notice_list.html', {
        'notices': notices,
        'interviews': interviews,
    })


def _is_placement_admin(user):
    if user.is_superuser:
        return True
    profile = getattr(user, 'profile', None)
    return profile and profile.is_placement_admin


@login_required
def admin_notices(request):
    if not _is_placement_admin(request.user):
        messages.error(request, 'Placement admin access required.')
        return redirect('jobs:dashboard')

    notices = Notice.objects.filter(posted_by=request.user)
    interviews = InterviewSchedule.objects.filter(posted_by=request.user)
    return render(request, 'notices/admin_panel.html', {
        'notices': notices,
        'interviews': interviews,
    })


@login_required
def admin_notice_create(request):
    if not _is_placement_admin(request.user):
        return redirect('jobs:dashboard')

    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user
            notice.save()
            messages.success(request, 'Notice published.')
            return redirect('notices:admin')
    else:
        form = NoticeForm()

    return render(request, 'notices/notice_form.html', {'form': form, 'title': 'Post Notice'})


@login_required
def admin_interview_create(request):
    if not _is_placement_admin(request.user):
        return redirect('jobs:dashboard')

    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.posted_by = request.user
            interview.save()
            messages.success(request, 'Interview schedule added.')
            return redirect('notices:admin')
    else:
        form = InterviewForm()

    return render(request, 'notices/interview_form.html', {'form': form, 'title': 'Schedule Interview'})
