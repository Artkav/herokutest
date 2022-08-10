from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', register_or_login_page, name='login-register'),
    path('task-list/', TaskList.as_view(), name='home'),
    path('detail/<int:pk>/', DetailTask.as_view(), name='task-detail'),
    path('statistics/', statistics, name='statistics'),
    path('create/', CreateTask.as_view(), name='create-task'),

    path('set_status/<int:pk>/<str:set_status>', set_status, name='set-status'),
]
