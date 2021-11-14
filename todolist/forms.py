from django.forms import ModelForm
from django import forms
from .models import ToDoList


class AddWorkForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'due_date', 'priority']
