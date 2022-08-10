from django import forms
from .models import Task
from datetime import date


class TaskCustomForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'full_text', 'deadline_date', 'status', 'priority', 'importance']
        widgets = {'deadline_date': forms.SelectDateWidget()}

    def clean_deadline_date(self):
        deadline = self.cleaned_data['deadline_date']
        today = date.today()
        if today > deadline:
            raise forms.ValidationError('Deadline must be later than today')
        return deadline
