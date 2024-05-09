from django.shortcuts import render, redirect
from django.http import HttpResponse
# permite establecer un formulario para crear un user
from django.contrib.auth.forms import UserCreationForm
# podemos importar el modelo user que se usa en el form
from django.contrib.auth.models import User
# podemos importar la libreria login para que python cree las cookies necesarias en nuestro navegador
from django.contrib.auth import login
# podemos importar los errores que pueda surgir
from django.db import IntegrityError

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
    return render(request, TASKS_VIEW_NAME)


def logout(request):
    return HttpResponse('Logout done')
