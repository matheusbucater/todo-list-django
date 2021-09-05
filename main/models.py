from django.db import models
from django.contrib.auth.models import User


class ToDoList(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)

	def __str__(self) -> str:

		return self.title

	def todos_count(self):
		return ToDoList.objects.filter(user=self.user).aggregate(models.Count('id'))['id__count']

	def get_tasks(self):

		tasks = ToDoList.objects.filter(pk=self.id).values_list('task__id', 'task__text', 'task__complete')
		return list(tasks)

	def tasks_count(self):
		return ToDoList.objects.filter(pk=self.id).aggregate(models.Count('task'))['task__count']

# task -> 1 todolist
# todolist -> * tasks
# task -> todolist : one to many

class Task(models.Model):

	todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
	text = models.CharField(max_length=255)
	complete = models.BooleanField(default=False)

	def __str__(self) -> str:

		return self.text
