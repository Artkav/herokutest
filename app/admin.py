from django.contrib import admin

from app.models import Task


class TaskAdmin(admin.ModelAdmin):

    # def short_text(self, obj):
    #     return obj.full_text[:30]

    list_display = ('name', 'short_text', 'owner',)
    search_fields = ('name',)
    list_filter = ('owner__first_name',)
    fields = ('name', 'full_text', 'owner', 'status', )
    readonly_fields = ('owner',)


admin.site.register(Task, TaskAdmin)
