# from celery import Celery
# from django.conf.global_settings import EMAIL_HOST_USER
# from django.contrib.auth import get_user_model
# from datetime import datetime, date, timedelta
from django.core.mail import send_mass_mail, send_mail
#
# User = get_user_model()
#
# app = Celery()
#
#
# @app.task
# def send_test_email():
#     # raise Exception('I am working')
#     send_mail(subject='subject', message='message text', from_email='email@email.com', recipient_list=['1email@emai.com'])
#
#
# @app.task
# def send_email_every_day():
#     # (subject, message, from_email, recipient_list)
#     data_for_mail = []
#     for user in User.objects.all():
#         message = f'Hello, {user.first_name.capitalize()}!'
#         tasks = user.tasks.filter(deadline_date=date.today() + timedelta(days=1))
#         if tasks.count():
#             message += ' Tomorrow is the deadline for those tasks:\n'
#             for task in tasks:
#                 message += f'\t{task.name}: {task.short_text}. \n'
#         message += 'We wish you to have time to do everything on time!'
#
#         data_for_mail.append(('To Do App remind you.', message, EMAIL_HOST_USER, [user.email]))
#
#     data_for_mail = tuple(data_for_mail)
#     send_mass_mail(datatuple=data_for_mail)
#
#
# @app.task
# def send_email_every_saturday():
#     data_for_mail = []
#     for user in User.objects.all():
#         message = f'Hello, {user.first_name.capitalize()}!'
#         end_date = datetime.now()
#         start_date = end_date - timedelta(days=7)
#         tasks = user.tasks.filter(finished_date__range=[start_date, end_date])
#         if tasks.count():
#             message += ' This week you completed such tasks :\n'
#             for task in tasks:
#                 message += f'\t{task.name}: {task.short_text}. \n'
#
#         data_for_mail.append(('Your finished tasss for this week', message, EMAIL_HOST_USER, [user.email]))
#
#     data_for_mail = tuple(data_for_mail)
#     send_mass_mail(datatuple=data_for_mail)


from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_test_email():
    # raise Exception('I am working')
    send_mail(subject='subject',
              message='message text',
              from_email='email@email.com',
              recipient_list=['1email@emai.com'])

#
# from celery import Celery
# from celery.schedules import crontab
#
# app = Celery()
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )
#
#
# @app.task
# def test(arg):
#     print(arg)
#
#
# @app.task
# def add(x, y):
#     z = x + y
#     print(z)
#     raise Exception('I am working')
#
# @app.task
# def send_test_email():
#     send_mail(subject='subject', message='message text', from_email='email@email.com', recipient_list=['1email@emai.com'])
