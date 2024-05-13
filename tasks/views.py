from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# permite establecer un formulario para crear o autenticar un user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# podemos importar el modelo user que se usa en el form
from django.contrib.auth.models import User
# podemos importar la libreria login para que python cree las cookies necesarias en nuestro navegador
from django.contrib.auth import login, logout, authenticate
# podemos importar los errores que pueda surgir
from django.db import IntegrityError
# importamos el form que creamos para crear una task
from .forms import TaskForm
from .models import Tasks

# constants
SINGUP_VIEW_NAME = "signup.html"
TASKS_VIEW_NAME = "tasks.html"

# Create your views here.


def home(request):
    """
        Return the home page of the application
    """
    return render(request, 'home.html')


def signup(request):
    """
        method: GET - Returns the user creation form to create a new user in DB
        method: POST - Verify the user information and create the user in DB
    """
    if request.method == 'GET':
        return render(request, SINGUP_VIEW_NAME, {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)  # guarda las cookies del usuario
                return redirect('tasks')
            except IntegrityError:
                return render(request, SINGUP_VIEW_NAME, {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })

        return render(request, SINGUP_VIEW_NAME, {
            'form': UserCreationForm,
            'error': 'Passwords do not match'
        })


def tasks(request):
    """
        Return the tasks view
    """
    tasks = Tasks.objects.filter(
        user=request.user,
        datecompleted__isnull=True
    )
    return render(request, TASKS_VIEW_NAME, {
        'tasks': tasks
    })


def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': TaskForm()
        })
    else:
        try:
            form = TaskForm(request.POST)
            print('Form: ', form)
            # el commit=False nos permite crear el objeto sin guardarlo directamente
            # esto para poder editar el objeto antes de guardarlo definitivamente
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm(),
                'error': 'Please provide valid data'
            })


def task_detail(request, id):
    # obtain the task from db
    task = get_object_or_404(Tasks, pk=id, user=request.user)
    if request.method == 'GET':
        # define the form with the task information
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()  # saves the new task date
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': "Somethings wrong"
            })


def complete_task(request, id):
    task = get_object_or_404(Tasks, pk=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


def delete_task(request, id):
    # Obtain the task to delete
    task = get_object_or_404(Tasks, pk=id, user=request.user)
    if request.method == 'POST':
        task.delete()  # delete the task
        return redirect('tasks')


def signout(request):
    # logout session
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        # Show the login form
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # Verify if the user is valid
        # Return None if user is invalid
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is None:
            # user is not valid
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password are incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
