from django.shortcuts import render


def adminLogin(request):
    return render(request, "admin_home.html")
