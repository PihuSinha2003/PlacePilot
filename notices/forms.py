from django import forms

from .models import InterviewSchedule, Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'content', 'is_pinned')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = InterviewSchedule
        fields = ('title', 'company', 'job', 'scheduled_date', 'scheduled_time', 'venue', 'notes')
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
