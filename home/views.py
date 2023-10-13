from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import smtplib, ssl
from email.message import EmailMessage
from random import randint
from . import models
import googlemaps

import requests
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token


# send mail
def send_otp(reciver_email):
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


def send_joinreq(joiner:models.JoinDetail):
    reciver_email = 'k.s.pranav.2004@gmail.com'
    port = 465
    password = 'ffdy tmgh xput wujz'
    subject = "Leo-Call-Taxi OTP"
    body = f"\t*New Join Request* \n\tFrom {joiner.name}\n\tContact :\n\t\tEmail : {joiner.email}\n\t\tPhone:{joiner.phone}"
    em = EmailMessage()
    em['From'] = 'eyeharshraj@gmail.com'
    em['To'] = reciver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
        smtp.login('eyeharshraj@gmail.com', password)
        smtp.sendmail('eyeharshraj@gmail.com', reciver_email, em.as_string())



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
        booking.otp = send_otp(booking.email)
        booking.save()
        print(booking.id)
        request.session["id"] = booking.id
        request.session["email"] = booking.email
        return render(request, "otpview.html")
    else:
        return redirect("/")



# codes to autocomplete place names and generate pincode for given place name and to calculate distance between two pincodes
#.....................................................................

# Replace 'YOUR_API_KEY' with your actual Google API key
gmaps = googlemaps.Client(key='AIzaSyCX2XkLAJIAs46WYurIDpwWcgMgeDqY11c')

def autocomplete_address(query):
    try:
        places = gmaps.places_autocomplete(query)
        return [place['description'] for place in places]
    except Exception as e:
        print(f"Error: {str(e)}")
        return []


#.......................................................................








def about(request):
    return render(request, "about.html")


def joinus(request):
    return render(request, "joinus.html")


def join(request):
    joinobj = models.JoinDetail()
    joinobj.name = request.POST.get("name")
    joinobj.email = request.POST.get("email")
    joinobj.phone = request.POST.get("phone")
    joinobj.save()
    send_joinreq(joinobj)
    request.session["status"] = False
    return redirect("/#joinreq")


def verify(request):
    if request.method == "POST":
        obj = models.BookingDetails.objects.filter(id=request.session["id"]).first()
        print(obj.id)
        if request.POST.get("OTP") == obj.otp:
            obj.verified = True
            obj.save()
            return render(request, "booked.html")
        else:
            messages.info(request, message='invalid otp')
            return render(request, "otpview.html", {"notvalid": True})
    else:
        redirect("book")


def calculate_price(request):
    return None