from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt


def adminLogin(request):
    return render(request, "adminlogin.html")

def contactdev(request):
    return render(request,"contactdev.html")

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, "admin_home.html", {"user": user})
        else:
            messages.info(request, "invalid credentials")
            return render(request, "adminlogin.html")
    else:
        return render(request,"admin_home.html")


def logout(request):
    return render(request,"logout.html")