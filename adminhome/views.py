import django.conf
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from home import models as homemodel
import smtplib, ssl
from email.message import EmailMessage

def adminLogin(request):
    return render(request, "adminlogin.html")


def contactdev(request):
    if request.method == "POST":
        reciver_email = 'codecraftersog@gmail.com'
        port = 465
        password = 'ffdy tmgh xput wujz'
        subject = "Leo-Call-Taxi OTP"
        body = f"Dev Support Request from : LeoCallTaxi \n\n {request.POST.get('body')}"
        em = EmailMessage()
        em['From'] = 'eyeharshraj@gmail.com'
        em['To'] = reciver_email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
            smtp.login('eyeharshraj@gmail.com', password)
            smtp.sendmail('eyeharshraj@gmail.com', reciver_email, em.as_string())

        return render(request, "admin_home.html")
    else:
        if auth.get_user(request).is_authenticated:
            return render(request, "contactdev.html")
        else:
            return login(request)


def login(request):
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
        return redirect("adminlogin")


def bookingdetails(request):
    obj = homemodel.BookingDetails.objects.filter(pickupdate__gte=date.today())
    return render(request, "bookdetails.html", {"bookingdetails": obj})


