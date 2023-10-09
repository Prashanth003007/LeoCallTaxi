from django.shortcuts import render, redirect
import smtplib, ssl
from email.message import EmailMessage
from random import randint
from . import models
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token


# send mail
def send_mail(reciver_email):
    txt = str(randint(100000, 999999))
    port = 465
    password = 'ffdy tmgh xput wujz'
    subject = "Leo-Call-Taxi OTP"
    body = f"Thank you for choosing Leo Call Taxi your otp for leo call taxi booking is{txt}"
    em = EmailMessage()
    em['From'] = 'eyeharshraj@gmail.com'
    em['To'] = reciver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
        smtp.login('eyeharshraj@gmail.com', password)
        smtp.sendmail('eyeharshraj@gmail.com', reciver_email, em.as_string())
    return txt


# Create your views here.
def userHome(request):
    return render(request, "user_home.html")


def book(request):
    return render(request, "booking.html")


def booked(request):
    if request.method == "POST":
        booking = models.BookingDetails()
        # Print the values of all the form fields
        booking.name = request.POST.get("name")
        booking.phone = request.POST.get("phoneno")
        booking.pickupdate = request.POST.get("date")
        booking.pickuptime = request.POST.get("time")
        booking.pickup = request.POST.get("pickup")
        booking.dropoff = request.POST.get("dropoff")
        booking.chooseride = request.POST.get("chooseride")
        booking.email = request.POST.get("email")
        booking.twoway = request.POST.get("twoways") == "on"
        print("Name:", booking.name)
        print("Phone Number:", booking.phone)
        print("Date:", booking.pickupdate)
        print("Time:", booking.pickupdate)
        print("Pickup:", booking.pickup)
        print("Drop Off:", booking.dropoff)
        print("Choose Ride:", booking.chooseride)
        print("twoways :", booking.twoway)
        booking.otp = send_mail(booking.email)
        booking.save()
        print(booking.id)
        return render(request, "booked.html", {"email": booking.email, "id": booking.id})
    else:
        return redirect("/")


def about(request):
    return render(request, "about.html")


def joinus(request):
    return render(request, "joinus.html")



def join(request):
    name = request.POST.get("name")
    return render(request, "user_home.html")
