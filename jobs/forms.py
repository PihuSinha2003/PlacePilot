from django import forms

from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company', 'job_type', 'role', 'location', 'description',
            'required_skills', 'min_batch_year', 'max_batch_year',
            'experience_level', 'salary', 'deadline', 'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'required_skills': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Python, Django, SQL'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
