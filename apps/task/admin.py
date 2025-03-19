from django.contrib import admin
from apps.task.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'user',
        'description',
        'important',
    ]
    ordering = ['id',]
    readonly_fields = ['creation_date',]
