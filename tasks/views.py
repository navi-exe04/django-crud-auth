from django.shortcuts import render
from django.http import HttpResponse
# permite establecer un formulario para crear un user
from django.contrib.auth.forms import UserCreationForm
# podemos importar el modelo user que se usa en el form
from django.contrib.auth.models import User

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
        return render(request, 'signup.html', {
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
                return HttpResponse('User created successfully')
            except:
                return HttpResponse('Username already exists')

        return HttpResponse('Password do not match')
