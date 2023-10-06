from django.shortcuts import render, redirect


# Create your views here.
def userHome(request):
    return render(request, "user_home.html")


def book(request):
    return render(request, "booking.html")


def booked(request):
    print(request.POST["name"])
    return render(request, "booked.html")


def about(request):
    return render(request, "about.html")


def joinus(request):
    return render(request, "joinus.html")
