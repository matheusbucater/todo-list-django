from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import models
from . import forms

@login_required
def delete_task(response, task_id, list_id):
    task = models.Task.objects.get(pk=task_id)
    task.delete()
    return HttpResponseRedirect(f'/{list_id}')

@login_required
def add_task(response, list_id):
    task = response.POST.get('textfield')
    new_task = models.Task(todo_list_id=list_id, text=task)
    new_task.save()
    return HttpResponseRedirect(f'/{list_id}')

@login_required
def complete_uncomplete_task(response, task_id, list_id):
    task = models.Task.objects.get(pk=task_id)
    task.complete = not task.complete
    task.save()
    return HttpResponseRedirect(f'/{list_id}')

@login_required
def index(response, id):
    user = response.user
    url = response.path
    # if response.method == 'POST' and 'new_task' in response.POST:
    #     task = response.POST.get('textfield')
    #     new_task = models.Task(todo_list_id=id, text=task, complete=False)
    #     new_task.save()
    # if response.method == 'POST' and 'delete_task' in response.POST:
    #     delete_task(response, id, url)
    todo_list = models.ToDoList.objects.get(pk=id, user=user)
    return render(response, 'list.html', { 'user': user, 'todo_list': todo_list, 'url': url })


@login_required
def home(response):
    user = response.user
    todo_list = models.ToDoList.objects.filter(user=user)
    list_url = 'http://localhost:8000'
    return render(response, 'home.html', { 'user': user, 'todo_list': list(todo_list), 'list_url': list_url })


@login_required
def create(response):
    user = response.user
    if response.method == 'POST':
        form = forms.CreateNewListForm(response.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            task = form.cleaned_data['task']
            todo_list = models.ToDoList(user=user, title=title)
            todo_list.save()
            new_task = models.Task(todo_list=todo_list  , text=task, complete=False)
            new_task.save()
            return index(response, todo_list.pk)
    else:
        form = forms.CreateNewListForm()
    return render(response, 'create.html', { 'user': user, 'form': form })

@login_required
def delete_todo_list(response, list_id):
    user = response.user
    todo_list = models.ToDoList.objects.get(user=user, pk=list_id)
    todo_list.delete()
    return HttpResponseRedirect('/')
