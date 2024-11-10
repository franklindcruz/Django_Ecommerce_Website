from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from estore.forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('home')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            if User.objects.filter(username=request.POST['username']).exists():
                messages.error(request, 'Username already exists')
            else:
                messages.error(request, 'Registration failed')
    return render(request, 'estore/auth/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Login failed!!! Check Credentials')
            return render(request, 'estore/auth/login.html')
    return render(request, 'estore/auth/login.html')


def logout(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, 'You are not logged in to perform this action')
        return redirect('login')
    auth_logout(request)
    messages.success(request, 'Logout successful')
    return redirect('login')
