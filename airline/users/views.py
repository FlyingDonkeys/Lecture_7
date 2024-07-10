import django.contrib.auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    # Check if the user is signed in
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'users/user.html')

def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django.contrib.auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'users/login.html', {
                "message": "Invalid Credentials"
            })

    return render(request, 'users/login.html')

def logout(request):
    django.contrib.auth.logout(request)
    return render(request, 'users/login.html', {
        "message": "You have been logged out."
    })

