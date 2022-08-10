from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from app.forms import TaskCustomForm
from app.models import Task

from app.tasks import send_test_email


def register_or_login_page(request):
    return render(request, 'app/home.html')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'app/home.html'
    login_url = 'app:login-register'
    paginate_by = 3


    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class DetailTask(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'app/task_detail.html'
    context_object_name = 'task'
    login_url = 'app:login-register'


class CreateTask(LoginRequiredMixin, CreateView):
    form_class = TaskCustomForm
    template_name = 'app/create_task.html'
    login_url = 'app:login-register'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return redirect('app:home')


def set_status(request, pk, set_status):
    task = Task.objects.get(id=pk)

    if set_status == 'finished':
        task.set_status_finished()
    elif set_status == 'todo':
        task.set_status_todo()
    elif set_status == 'in_progress':
        task.set_status_in_progress()
    elif set_status == 'blocked':
        task.set_status_blocked()

    task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def statistics(request):

    '''Celery test'''

    # send_test_email.delay()
    ''' End celery test '''

    tasks = Task.objects.filter(owner=request.user)
    finished_tasks = tasks.exclude(finished_date__isnull=True)
    statistics_bool = False

    try:
        time_delta = sum([(task.finished_date - task.created_date).seconds for task in finished_tasks])
        average_duration_of_the_task = time_delta // finished_tasks.count()
    except ZeroDivisionError:
        average_duration_of_the_task = 0
        statistics_bool = True

    context = {
        'all_tasks': tasks.count(),
        'status_todo': tasks.filter(status='todo').count(),
        'status_in_progress': tasks.filter(status='in_progress').count(),
        'status_blocked': tasks.filter(status='blocked').count(),
        'status_finished': tasks.filter(status='finished').count(),
        'average_duration_of_the_task':
            f'{average_duration_of_the_task//3600} hours '
            f'{(average_duration_of_the_task//60)%60} minutes',
        'statistic': statistics_bool,
    }
    return render(request, 'app/staistics.html', context=context)
