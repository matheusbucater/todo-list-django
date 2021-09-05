from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings


urlpatterns = [
    path('<int:id>', views.index, name='index'),
    path('add-task/<int:list_id>', views.add_task),
    path('delete-task/<int:task_id>/<int:list_id>', views.delete_task),
    path('complete-uncomplete-task/<int:task_id>/<int:list_id>', views.complete_uncomplete_task),
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('delete-todo-list/<int:list_id>/', views.delete_todo_list, name='delete_todo_list'),
    path('acc/logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
