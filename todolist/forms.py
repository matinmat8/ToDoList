from django.forms import ModelForm
from django import forms
from .models import ToDoList, PRIORITY_CHOICES


class AddWorkForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'due_date', 'priority']


class FilterForm(forms.Form):
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    due_date = forms.DateTimeField(required=False)
    done = forms.BooleanField(required=False)

