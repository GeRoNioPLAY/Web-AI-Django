from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistration, UserLogin, UserDataChange, RegisterForm
from .models import CustomUser

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistration(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('list')
#     else:
#         form = UserRegistration()
#     return render(request, 'authapp/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = CustomUser(username=username, email=email)
            user = CustomUser(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
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

