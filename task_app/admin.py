from django.contrib import admin
from task_app.models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date',
                    'created_by', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'created_by__username')
    list_filter = ('start_date', 'end_date', 'created_by')
    ordering = ('-created_at',)
    date_hierarchy = 'start_date'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'start_date',
                    'due_date', 'assigned_to', 'project', 'created_at', 'updated_at')
    search_fields = ('title', 'description',
                     'assigned_to__username', 'project__name')
    list_filter = ('status', 'priority', 'start_date',
                   'due_date', 'assigned_to', 'project')
    ordering = ('-created_at',)
    date_hierarchy = 'start_date'
