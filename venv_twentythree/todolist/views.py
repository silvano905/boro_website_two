from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DeleteView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib import messages
from comments.models import Suggestion
from .models import Todo
User = get_user_model()
from posts.models import MakePost
from .forms import TodoForm, TestingForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain


@login_required
def addTodo(request):
    todo_list = Todo.objects.filter(user__exact=request.user)
    form = TodoForm()

    if request.method == "POST":
        form = TodoForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user_todo_list = form.save(commit=False)
            get_title = form.cleaned_data['title']
            user_todo_list.user = request.user
            if_obj_exists = Todo.objects.filter(title=get_title, user__exact=request.user).exists()
            if if_obj_exists:
                messages.warning(request, 'Warning already in your list!')
                form = TodoForm()  # to clear form input
                return render(request, 'todolist/index.html', context={'form': form, 'todo_list': todo_list})
            else:
                user_todo_list.save()
                form = TodoForm()   # to clear form input
                return render(request, 'todolist/index.html', context={'form': form, 'todo_list': todo_list})

        else:
            return render(request, 'todolist/index.html', context={'form': form, 'todo_list': todo_list})
    else:
        context = {'todo_list': todo_list, 'form': form}
        return render(request, 'todolist/index.html', context)


@login_required
def complete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    user = request.user
    if user == todo.user:
        todo.complete = True
        todo.save()

    return redirect('todolist:add')


@login_required
def delete_completed(request):
    Todo.objects.filter(user__exact=request.user, complete__exact=True).delete()
    return redirect('todolist:add')


@login_required
def delete_all(request):
    Todo.objects.filter(user__exact=request.user).delete()

    return redirect('todolist:add')


class UserTodo(ListView, LoginRequiredMixin):

    context_object_name = 'todo_list'
    model = Todo
    template_name = 'todolist/user_todo_list.html'

    def get_queryset(self):
        try:
            self.todo_user = User.objects.prefetch_related('wishes').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.todo_user.wishes.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_user'] = self.todo_user
        return context


class TodoDetailView(DetailView, LoginRequiredMixin):
    context_object_name = 'todo'
    model = Todo
    template_name = 'todolist/todo_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TodoDetailView, self).get_context_data(**kwargs)
        context['suggestion_list'] = Suggestion.objects.all().order_by('-created_date')
        return context


class TodoListView(ListView, LoginRequiredMixin):
    context_object_name = 'todo_list'
    template_name = 'todolist/todo_list.html'
    model = Todo


@login_required
def world_todo_list(request):
    queryset_list = Todo.objects.all()
    query = request.GET.get('q')
    if query is not None:
        queryset_list = queryset_list.filter(Q(title__icontains=query) | Q(info__icontains=query))

    paginator = Paginator(queryset_list, 6)    # Show 25 contacts per page

    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    context = {
        "todo_list": queryset
    }
    return render(request, 'todolist/todo_list.html', context)


@login_required
def delete_individual_todo(request, pk):
    query = Todo.objects.filter(user__exact=request.user).get(pk=pk)

    query.delete()
    return redirect('todo:add')



