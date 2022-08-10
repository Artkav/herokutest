from datetime import datetime, timezone, timedelta

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import UpdateView

from app.models import Task
from users.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from .utils import send_email_for_verify
from django.contrib.auth.tokens import default_token_generator as token_generator

User = get_user_model()


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
        }
        return render(request, self.template_name, context=context)


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('app:login-register')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class MyLoginView(LoginView):
    form_class = AuthenticationForm


def confirm_email(request):
    return render(request, 'registration/confirm_email.html')


def invalid_verify(request):
    return render(request, 'registration/invalid_verify.html')


class EditUser(UpdateView):
    template_name = 'users/edit_user.html'
    model = User
    fields = ['first_name', 'last_name', 'position_in_company']
    success_url = reverse_lazy('app:home')



def custom_page(request):
    users_count = User.objects.all().count()
    tasks_count = Task.objects.all().count()
    tasks_status_todo = Task.objects.filter(status='todo').count()
    tasks_status_in_progress = Task.objects.filter(status='in_progress').count()
    tasks_status_blocked = Task.objects.filter(status='blocked').count()
    tasks_status_finished = Task.objects.filter(status='finished').count()
    last_registered_users = User.objects.filter(date_joined__gt=datetime.now(tz=timezone.utc) - timedelta(days=7)).count()
    context = {
        'users_count': users_count,
        'tasks_count': tasks_count,
        'tasks_status_todo': tasks_status_todo,
        'tasks_status_in_progress': tasks_status_in_progress,
        'tasks_status_blocked': tasks_status_blocked,
        'tasks_status_finished': tasks_status_finished,
        'last_registered_users': last_registered_users,
    }

    return render(request, 'app/my_custom_page.html', context=context)