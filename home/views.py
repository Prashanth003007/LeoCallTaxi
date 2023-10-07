from django.shortcuts import render, redirect


# Create your views here.
def userHome(request):
    return render(request, "user_home.html")


def book(request):
    return render(request, "booking.html")


def booked(request):
    # Print the values of all the form fields
    name = request.POST.get("name")
    phoneno = request.POST.get("phoneno")
    date = request.POST.get("date")
    time = request.POST.get("time")
    pickup = request.POST.get("pickup")
    dropoff = request.POST.get("dropoff")
    chooseride = request.POST.get("chooseride")
    twoways = request.POST.get("twoways")

    print("Name:", name)
    print("Phone Number:", phoneno)
    print("Date:", date)
    print("Time:", time)
    print("Pickup:", pickup)
    print("Drop Off:", dropoff)
    print("Choose Ride:", chooseride)
    print("twoways :" , twoways)

    return render(request, "booked.html")


def about(request):
    return render(request, "about.html")


def joinus(request):
    return render(request, "joinus.html")
