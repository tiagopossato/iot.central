from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from . import models

def login_view(request):
    if(request.method != 'POST'):
        return render(request, 'interface/login.html')
    try:
        username = request.POST.get('username')
        if(username == None):
            return render(request, 'interface/login.html', {'error':'True'})
        password = request.POST.get('password')
        if(password == None):
            return render(request, 'interface/login.html', {'error':'True'})
    except KeyError as e:
        return render(request, 'interface/login.html', {'error':'True'})
    # Autenticação
    try:
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'interface/login.html', {'error':'True'})
       
        login(request, user)
        return redirect('/')
    except Exception as e:
        return render(request, 'interface/login.html', {'error':'True'})

def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def index(request):
    return render(request, 'interface/index.html', {})