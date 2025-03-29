from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistration, UserLogin, UserDataChange

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


@login_required
def account(request):
    if request.method == 'POST':
        form = UserDataChange(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserDataChange(instance=request.user)
    return render(request, 'authapp/account.html', {'form': form})

