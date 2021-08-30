from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models import Count, F, Value
from . import models

class TaskInline(admin.TabularInline):

      model = models.Task
      min_num = 3
      extra = 0



@admin.register(models.ToDoList)
class ToDoListAdmin(admin.ModelAdmin):

	inlines = [TaskInline]
	list_display = ['title', 'tasks']

	
	def get_queryset(self, request):

		queryset = super().get_queryset(request)
		queryset = queryset.annotate(
			_tasks_count=Count('task'),
		)
		return queryset

	@admin.display(ordering="_tasks_count")
	def tasks(self, todo_list):	
		
		tasks = ''
		for task in todo_list.get_tasks():
			url = (reverse('admin:main_task_changelist')
				+ '?'
				+ urlencode({ 'id': str(task[0]) }))
			tasks += format_html('<a href="{}">{}</a>', url, task[1]) + '; '
		return format_html(tasks)


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):

	list_display = ['text', 'todo_lists', 'complete']
	list_editable = ['complete']

	@admin.display(ordering='todo_list__title')
	def todo_lists(self, task):
		url = (reverse('admin:main_todolist_changelist')
			+ '?'
			+ urlencode({ 'id': str(task.todo_list.id) }))
		return format_html('<a href="{}">{}</a>', url, task.todo_list.title)