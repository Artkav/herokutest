from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True,)
    username = models.CharField(blank=True, max_length=50)
    first_name = models.CharField(verbose_name="first name", max_length=150, default='')
    last_name = models.CharField(verbose_name="last name", max_length=150, default='')
    position_in_company = models.CharField(verbose_name="position in company", max_length=150, editable=True, default='')
    blocked = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_task_count(self):
        return self.tasks.all().count()
