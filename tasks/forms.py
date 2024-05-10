from django.forms import ModelForm
from .models import Tasks

# define the task form from the tasks model


class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'important']
