from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from . import models

def login_view(request):

    if(not request.POST):
        return render(request, 'central/login.html')

    username = request.POST['username']
    password = request.POST['password']
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'central/login.html', {'error':'True'})

def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def index(request):
    return render(request, 'central/index.html', {})
