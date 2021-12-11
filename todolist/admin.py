from django.contrib import admin
from .models import ToDoList, Comment


@admin.register(ToDoList)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('user', 'pk', 'title', 'due_date')
    search_fields = ('title', 'description', 'user', 'due_date', 'create_at')
    list_filter = ('user', 'create_at')
    prepopulated_fields = {'slug': ('title', 'description','priority')}


@admin.register(Comment)
class ToDoListAdmin(admin.ModelAdmin):
    list_display = ('user', 'for_work',)
    search_fields = ('user', 'for_work')
    list_filter = ('user', 'for_work')