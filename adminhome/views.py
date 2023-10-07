import django.conf
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, csrf_exempt,requires_csrf_token

def adminLogin(request):
    return render(request, "adminlogin.html")


def contactdev(request):
    if auth.get_user(request).is_authenticated:
        return render(request, "contactdev.html")
    else:
        return login(request)

def login(request):
    if auth.get_user(request).is_authenticated:
        return render(request, "admin_home.html")
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return render(request, "admin_home.html")
            else:
                messages.info(request, "invalid credentials")
                return render(request, "adminlogin.html")
        else:
            return render(request, "admin_home.html")


def logoutpage(request):
    if auth.get_user(request).is_authenticated:
        return render(request, "logout.html")
    else:
        return redirect("/")


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return adminLogin(request)
    else:
        return redirect("/")
