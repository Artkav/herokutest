from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from app.models import Task
from users.forms import UserCreationForm

User = get_user_model()


class TaskInline(admin.TabularInline):
    model = Task

    def short_text(self, obj):
        return obj.full_text[:50]

    fields = ('name', 'short_text')
    readonly_fields = ('name', 'short_text')
    extra = 0


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    def tasks_count(self, obj):
        return obj.tasks.all().count()

    ''' List user page '''

    list_display = ("first_name", "last_name", "position_in_company", "email", 'tasks_count', 'get_task_count')
    list_display_links = ('first_name', 'email')
    search_fields = ('first_name', 'last_name')

    '''Detail user page'''

    fields = ('first_name', 'last_name', 'email')
    fieldsets = None
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('first_name', 'last_name', 'email', "password1", "password2"),
            },
        ),
    )

    '''Readonly_fields'''

    def get_readonly_fields(self, request, obj=None):
        if obj:
            print(obj.tasks.all().count())
            obj.tasks_count = obj.tasks.all().count()
            return ['first_name', 'last_name', 'email', 'tasks_count']
        else:
            return []

    inlines = [TaskInline]