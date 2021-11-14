from django.shortcuts import redirect

from .models import ToDoList
from .forms import AddWorkForm

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class WorksList(ListView, LoginRequiredMixin):
    model = ToDoList
    template_name = 'todolist/works.html'

    def get_queryset(self):
        obj = super().get_queryset()
        return obj.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = super().get_context_data(**kwargs)
        object_list['form'] = AddWorkForm()
        return object_list

    def post(self, request, *args, **kwargs):
        obj = ToDoList.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            due_date=request.POST.get('due_date'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority'),
        )
        return redirect('todolist:list')