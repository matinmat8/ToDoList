from django.contrib import admin
from .models import ToDoList


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'due_date', 'reminder',)
    search_fields = ('title', 'description', 'user', 'due_date', 'create_at')
    list_filter = ('user', 'create_at')
    prepopulated_fields = {'slug': ('title', 'description','priority')}