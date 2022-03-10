




import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View

from .models import ToDoList, Comment
from .forms import AddWorkForm, FilterForm, CommentForm, UpdateWorkForm

from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView


def index(request):
    return render(request, 'todolist/base.html')


@method_decorator(login_required, name='dispatch')
class WorksList(ListView):
    model = ToDoList
    template_name = 'todolist/works.html'

    def get_queryset(self):
        obj = super().get_queryset()
        today = datetime.date.today()
        return obj.filter(user=self.request.user, due_date=today, tree=None).order_by('priority')

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

# Update works class based view!
# class UpdateWork(UpdateView):
#     model = ToDoList
#     fields = ['title', 'description', 'due_date', 'priority']
#     template_name_suffix = '_update_form'


def update_work(request, pk):
    obj = get_object_or_404(ToDoList, pk=pk)
    form = UpdateWorkForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            url = obj.get_absolute_url()
            form.save()
            return redirect(url)
    return render(request, 'todolist/todolist_update_form.html', context={'form': form})


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class DoneWork(View):
    def post(self, request, *args, **kwargs):
        work = ToDoList.objects.get(user=request.user, pk=kwargs['pk'])
        url = reverse('todolist:get_children', kwargs={'pk': self.kwargs['pk']})
        done = request.POST.get('done')
        page = request.POST.get('page')
        # Handle changing done field for filter page and return filter page
        if page == 'filter':
            if done == 'True':
                work.done = True
                work.save()
                return redirect('todolist:filter')
            else:
                work.done = False
                work.save()
            return redirect('todolist:filter')
        # Handle changing done field for children page and return children page
        else:
            if done == 'True':
                work.done = True
                work.save()
                return redirect(url)
            else:
                work.done = False
                work.save()
            return redirect(url)


@method_decorator(login_required, name='dispatch')
class DeleteWork(DeleteView):
    model = ToDoList
    success_url = reverse_lazy('todolist:list')


@method_decorator(login_required, name='dispatch')
class DeleteComment(DeleteView):
    model = Comment
    success_url = reverse_lazy('todolist:list')

    # Handle deleting without confirm page
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class FilterView(ListView):
    template_name = 'todolist/filter.html'
    today = datetime.date.today()

    def get_queryset(self):
        obj = ToDoList.objects.filter(user=self.request.user)
        return obj

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
        obj = self.get_queryset()
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
