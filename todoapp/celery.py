# import os
# from celery import Celery
#
# from celery.schedules import crontab
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoapp.settings')
#
# app = Celery('todoapp')
#
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# app.conf.beat_schedule = {
#     'send-email-every-60-seconds': {
#         'task': 'tasks.send_test_email',
#         'schedule': 30.0,
#     },
#     # 'send-email-every-day-at-8': {
#     #     'task': 'tasks.send_email_every_day',
#     #     'schedule': crontab(minute=0, hour=8),
#     # },
#     # 'send-email-every-saturday-at-8': {
#     #     'task': 'tasks.send_email_every_saturday',
#     #     'schedule': crontab(minute=0, hour=8, day_of_week='saturday'),
#     # }
#
#
# }
# app.conf.timezone = 'UTC'
#
# app.autodiscover_tasks()
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')













import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todoapp.settings')

app = Celery('todoapp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.send_test_email',
        'schedule': 30.0,
    },
}
app.conf.timezone = 'UTC'