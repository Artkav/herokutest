from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from datetime import datetime as dt


User = get_user_model()


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    name = models.CharField(max_length=250)
    full_text = models.TextField()
    deadline_date = models.DateField(null=True, blank=True)
    finished_date = models.DateTimeField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=(
            ('todo', 'To do'),
            ('in_progress', 'In progress'),
            ('blocked', 'Blocked'),
            ('finished', 'Finished'),
        ), default='todo', max_length=20)
    priority = models.CharField(
        choices=(
            ('low', 'Low'),
            ('high', 'High'),
            ('medium', 'Medium'),
        ), default='medium', max_length=6)
    importance = models.BooleanField(default=False)

    def url(self):
        return reverse('app:task-detail', kwargs={'pk': self.id})

    def set_status_finished(self):
        self.status = 'finished'
        self.finished_date = dt.now()

    def set_status_todo(self):
        self.status = 'todo'

    def set_status_in_progress(self):
        self.status = 'in_progress'

    def set_status_blocked(self):
        self.status = 'blocked'

    def short_text(self):
        return self.full_text[:50]

    class Meta:
        ordering = ['deadline_date', 'created_date']
