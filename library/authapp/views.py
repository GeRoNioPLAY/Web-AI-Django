from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistration, UserLogin

def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list')
    else:
        form = UserRegistration()
    return render(request, 'authapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLogin(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list')
    else:
        form = UserLogin()
    return render(request, 'authapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('list')

