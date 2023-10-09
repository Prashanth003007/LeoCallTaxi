from django.shortcuts import render, redirect
import smtplib, ssl
from email.message import EmailMessage
from random import randint

from django.template import RequestContext
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, csrf_exempt,requires_csrf_token

#send mail
def send_mail(reciver_email):
    txt = str(randint(1000, 9999))
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
        smtp.login('eyeharshraj@gmail.com', 'ffdy tmgh xput wujz')
        smtp.sendmail('eyeharshraj@gmail.com', reciver_email, em.as_string())
    return txt

# Create your views here.
def userHome(request):
    return render(request, "user_home.html")


def book(request):
    return render(request, "booking.html")


def booked(request):
    if request.method == "POST":
        if request.GET.get("otpsent"):
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
            print("twoways :", twoways)
            return render(request, "booked.html")
        else:
            return render(request,"booking.html",{"otpsent":True})
    else:
        return redirect("/")


def about(request):
    return render(request, "about.html")


def joinus(request):
    return render(request, "joinus.html")

@cache_control()
def join(request):
    name = request.POST.get("name")
    return render(request,"user_home.html")