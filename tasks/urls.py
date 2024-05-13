from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks_completed/', views.task_completed, name="tasks_completed"),
    path('tasks/create', views.create_task, name="create_task"),
    path('tasks/<int:id>', views.task_detail, name="task_detail"),
    path('tasks/complete/<int:id>', views.complete_task, name="complete_task"),
    path('tasks/delete/<int:id>', views.delete_task, name="delete_task"),
    path('signout/', views.signout, name="signout"),
    path('signin/', views.signin, name="signin"),
]
