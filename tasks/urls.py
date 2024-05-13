from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/create', views.create_task, name="create_task"),
    path('tasks/<int:id>', views.task_detail, name="task_detail"),
    path('tasks/delete/<int:id>', views.delete_task, name="delete_task"),
    path('signout/', views.signout, name="signout"),
    path('signin/', views.signin, name="signin"),
]
