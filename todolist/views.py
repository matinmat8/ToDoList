import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .models import ToDoList, Comment
from .forms import AddWorkForm, FilterForm

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class WorksList(ListView, LoginRequiredMixin):
    model = ToDoList
    template_name = 'todolist/works.html'

    def get_queryset(self):
        obj = super().get_queryset()
        today = datetime.date.today()
        return obj.filter(user=self.request.user, due_date=today)

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
        obj.save()
        return redirect('todolist:list')


@method_decorator(login_required, name='dispatch')
class GetChildren(View):
    def get(self, *args, **kwargs):
        work = ToDoList.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        comments = Comment.objects.filter(user=self.request.user, for_work=work)
        children = work.children.all()
        return render(self.request, 'todolist/children.html', {'children': children, 'work': work, 'comments': comments})


class FilterView(ListView, LoginRequiredMixin):
    template_name = 'todolist/filter.html'
    today = datetime.date.today()

    def get_queryset(self):
        queryset = ToDoList.objects.filter(user=self.request.user, due_date=self.today)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm()
        return context

    def post(self, request):
        form = FilterForm(data=request.POST)
        get_field = lambda f: request.POST.get(f)
        due_date = get_field('due_date')
        priority = get_field('priority')
        done = get_field('done')
        user = request.user
        obj = ToDoList.objects.filter(user=user)
        if due_date:
            obj = obj.filter(due_date=due_date)
        else:
            pass
        if priority:
            obj = obj.filter(priority=priority)
        else:
            pass
        if done == 'on':
            done = True
        else:
            done = False
        if done:
            obj = obj.filter(done=done)
        else:
            pass
        return render(request, template_name='todolist/filter.html', context={'object_list': obj, 'form': form})