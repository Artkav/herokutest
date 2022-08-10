release: python manage.py migrate
web: gunicorn todoapp.wsgi
celery: celery -A todoapp.celery worker -l INFO
celerybeat: celery -A todoapp beat -l INFO