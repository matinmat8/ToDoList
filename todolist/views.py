from .models import ToDoList

from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class Works(ListView, LoginRequiredMixin):
    model = ToDoList
    template_name = 'todolist/works.html'

    def get_queryset(self):
        obj = super().get_queryset()
        return obj.filter(user=self.request.user)