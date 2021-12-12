import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from .models import ToDoList, Comment
from .forms import AddWorkForm, FilterForm, CommentForm

from django.views.generic import ListView
from django.views.generic.edit import DeleteView


def index(request):
    return render(request, 'todolist/base.html')


@method_decorator(login_required, name='dispatch')
class WorksList(ListView):
    model = ToDoList
    template_name = 'todolist/works.html'

    def get_queryset(self):
        obj = super().get_queryset()
        today = datetime.date.today()
        return obj.filter(user=self.request.user, due_date=today, tree=None)

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
        form = AddWorkForm()
        comment_form = CommentForm()
        work = ToDoList.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        comments = Comment.objects.filter(user=self.request.user, for_work=work)
        children = work.children.all()
        return render(self.request, 'todolist/children.html', {'children': children, 'work': work,
                                                               'comments': comments, 'form': form,
                                                               'comment_form': comment_form})

    def post(self, *args, **kwargs):
        request = self.request
        work = ToDoList.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        obj = ToDoList.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            tree=work,
            due_date=request.POST.get('due_date'),
            description=request.POST.get('description'),
            priority=request.POST.get('priority'),
        )
        obj.save()
        url = work.get_absolute_url()
        return redirect(url)


class AddComment(View):
    def post(self, request, *args, **kwargs):
        work = ToDoList.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        obj = Comment.objects.create(
            for_work=work,
            user=request.user,
            comment=request.POST.get('comment')
        )
        obj.save()
        url = work.get_absolute_url()
        return redirect(url)


class DeleteWork(DeleteView):
    model = ToDoList
    success_url = reverse_lazy('todolist:list')


@method_decorator(login_required, name='dispatch')
class FilterView(ListView):
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