from django.contrib.admin.options import IS_POPUP_VAR
from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from app.models import Task
from users.forms import UserCreationForm
from users.utils import send_email_for_verify

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

    """Override method response_add for sending email for verify, when User created from admin panel"""

    def response_add(self, request, obj, post_url_continue=None):

        send_email_for_verify(request, obj)

        if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
            request.POST = request.POST.copy()
            request.POST['_continue'] = 1
        return super().response_add(request, obj, post_url_continue)


    def tasks_count(self, obj):
        return obj.tasks.all().count()

    ''' List user page '''

    list_display = ("first_name", "last_name", "position_in_company", "email", 'tasks_count')
    list_display_links = ('first_name', 'email')
    search_fields = ('first_name', 'last_name')

    '''Detail user page'''
    fields = ('first_name', 'last_name', 'email', 'tasks_count')
    fieldsets = None

    '''Create user form in admin panel'''

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ('email', 'first_name', 'last_name', 'position_in_company', "password1", "password2"),
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
