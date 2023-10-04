from django.shortcuts import render, redirect


# Create your views here.
def userHome(request):
    return render(request, "user_home.html")


def book(request):
    return render(request, "booking.html")
