import csv

import django.conf
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
from home import models as homemodel
import smtplib, ssl
from email.message import EmailMessage


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminLogin(request):
    return render(request, "adminlogin.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contactdev(request):
    if not request.user.is_authenticated or request.session.get('page_token') is None:
        # Handle unauthorized access or redirection here
        return redirect('adminlogin')
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutpage(request):
    if not request.user.is_authenticated or request.session.get('page_token') is None:
        redirect("adminlogin")
    if auth.get_user(request).is_authenticated:
        return render(request, "logout.html")
    else:
        return redirect("adminlogin")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if not request.user.is_authenticated or request.session.get('page_token') is None:
        # Handle unauthorized access or redirection here
        return redirect('adminlogin')

    auth.logout(request)
    return redirect("adminlogin")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bookingdetails(request):
    if not request.user.is_authenticated or request.session.get('page_token') is None:
        # Handle unauthorized access or redirection here
        return redirect('adminlogin')
    emailExportAll()
    obj = homemodel.BookingDetails.objects.filter(pickupdate__gte=date.today(),verified=True)
    return render(request, "bookdetails.html", {"bookingdetails": obj})

def emailExportWeek():
    obj = homemodel.BookingDetails.objects.filter(verified=True,pickupdate__gte=date.today(),pickupdate__lt=date.today()).all()
    port = 465
    password = 'ffdy tmgh xput wujz'
    # Generate the CSV file
    csv_data = []
    for row in obj:
        csv_data.append([row.name, row.phone, row.email, row.pickupdate,
                         row.pickuptime, row.pickup, row.dropoff,
                         row.twoway, row.ride, row.efare])

    csv_file_path = "mydata.csv"
    with open(csv_file_path, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'Phone', 'Email', 'PickupDate',
                             'PickupTime', 'From', 'To', 'TwoWay', "Ride", "Est"])
        csv_writer.writerows(csv_data)

    # ... (The rest of your code)

    # Attach the CSV file to the email
    em = EmailMessage()
    em['From'] = 'eyeharshraj@gmail.com'
    em['To'] = "k.s.pranav.2004@gmail.com"
    em['Subject'] = "Exported Data"
    em.set_content("Data export attached", subtype="plain")

    # Attach the CSV file
    with open(csv_file_path, 'rb') as csv_file:
        em.add_attachment(csv_file.read(), filename="mydata.csv" , maintype="application", subtype="csv")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
        smtp.login('eyeharshraj@gmail.com', password)
        smtp.sendmail('eyeharshraj@gmail.com', "k.s.pranav.2004@gmail.com", em.as_bytes())
def emailExportAll():
    obj = homemodel.BookingDetails.objects.filter(verified=True).all()
    port = 465
    password = 'ffdy tmgh xput wujz'
    # Generate the CSV file
    csv_data = []
    for row in obj:
        csv_data.append([row.name, row.phone, row.email, row.pickupdate,
                         row.pickuptime, row.pickup, row.dropoff,
                         row.twoway, row.ride, row.efare])

    csv_file_path = "mydata.csv"
    with open(csv_file_path, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'Phone', 'Email', 'PickupDate',
                             'PickupTime', 'From', 'To', 'TwoWay', "Ride", "Est"])
        csv_writer.writerows(csv_data)

    # ... (The rest of your code)

    # Attach the CSV file to the email
    em = EmailMessage()
    em['From'] = 'eyeharshraj@gmail.com'
    em['To'] = "k.s.pranav.2004@gmail.com"
    em['Subject'] = "Exported Data"
    em.set_content("Data export attached", subtype="plain")

    # Attach the CSV file
    with open(csv_file_path, 'rb') as csv_file:
        em.add_attachment(csv_file.read(), filename="mydata.csv" , maintype="application", subtype="csv")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
        smtp.login('eyeharshraj@gmail.com', password)
        smtp.sendmail('eyeharshraj@gmail.com', "k.s.pranav.2004@gmail.com", em.as_bytes())