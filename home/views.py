import json

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


# Create your views here.
def userHome(request):
    return render(request, "user_home.html")


def book(request):
    return render(request, "booking.html",{"cars":models.Cars.objects.all()})


def book2(request):
    return render(request,"booking2.html",{"cars":models.Cars.objects.all()})


def prebook(request):
    return render(request,"prebooking.html")

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


def send_joinreq(joiner: models.JoinDetail):
    reciver_email = 'k.s.pranav.2004@gmail.com'
    port = 465
    password = 'ffdy tmgh xput wujz'
    subject = "Leo-Call-Taxi OTP"
    body = f"\t*New Join Request* \n\tFrom {joiner.name}\n\tContact :\n\t\tEmail : {joiner.email}\n\t\tPhone:{joiner.phone}"+\
           f"\n\t\tRegistration no : {joiner.regno}\n\t\tModel : {joiner.modeltype}"
    em = EmailMessage()
    em['From'] = 'eyeharshraj@gmail.com'
    em['To'] = reciver_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as smtp:
        smtp.login('eyeharshraj@gmail.com', password)
        smtp.sendmail('eyeharshraj@gmail.com', reciver_email, em.as_string())





def calculate_distance(origin, destination):
    try:
        directions = gmaps.directions(origin, destination)
        if directions:
            route = directions[0]['legs'][0]
            return route['distance']['text']
        else:
            return "1000000000"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "1000000000"

def calculate_fare(distance,type,twoway):
    cost = 0
    car = models.Cars.objects.filter(code=type).first()
    if distance < 20:
        distance -= car.base_d_i
        cost += car.basefare_i
        if distance > 0:
            cost += car.add_charge_i * distance
    else:
        distance -= car.base_d_o
        cost += car.basefare_o
        if distance > 0:
            cost += car.add_charge_o * distance
    if twoway:
        return cost * 2
    else:
        return cost

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
        booking.ride = request.POST.get("chooseride")
        booking.email = request.POST.get("email")
        booking.twoway = request.POST.get("twoways") == "on"
        booking.efare = calculate_fare(int(float("".join((calculate_distance(booking.pickup,booking.dropoff)[:-3]).split(",")))),
                                       booking.ride,booking.twoway)

        booking.otp = send_otp(booking.email)
        booking.save()
        print(booking.id)
        request.session["id"] = booking.id
        request.session["email"] = booking.email
        return render(request, "otpview.html")
    else:
        return redirect("/")


# codes to autocomplete place names and generate pincode for given place name and to calculate distance between two pincodes
# .....................................................................

# Replace 'YOUR_API_KEY' with your actual Google API key
gmaps = googlemaps.Client(key='AIzaSyCX2XkLAJIAs46WYurIDpwWcgMgeDqY11c')


def autocomplete_address(query):
    try:
        places = gmaps.places_autocomplete(query)
        return [place['description'] for place in places]
    except Exception as e:
        print(f"Error: {str(e)}")
        return []


# .......................................................................


def about(request):
    return render(request, "about.html")


def joinus(request):
    return render(request, "joinus.html")


def join(request):
    joinobj = models.JoinDetail()
    joinobj.name = request.POST.get("name")
    joinobj.email = request.POST.get("email")
    joinobj.phone = request.POST.get("phone")
    joinobj.regno = request.POST.get("carregno")
    joinobj.modeltype = request.POST.get("carmodel")
    joinobj.save()
    send_joinreq(joinobj)
    request.session["status"] = False
    return redirect("/#joinreq")


def verify(request):
    if request.method == "POST":
        obj = models.BookingDetails.objects.filter(id=request.session["id"]).first()
        if request.POST.get("OTP") == obj.otp:
            obj.verified = True
            obj.save()
            return render(request, "booked.html")
        else:
            messages.info(request, message='invalid otp')
            return render(request, "otpview.html", {"notvalid": True})
    else:
        redirect("book")


@csrf_exempt
def calculate_price(request):
    if request.method == "POST":
        print("In")
        data = json.loads(request.body)
        car = models.Cars.objects.filter(code=data.get("type")).first()
        twoway = data.get("twoway")
        distance = float("".join((data.get("distance")[:-3]).split(",")))
        del data
        if not car:
            return JsonResponse({"error": "Car not found"})

        time = int(distance//30)
        cost = 0

        if distance < 20:
            distance -= car.base_d_i
            cost += car.basefare_i
            if distance > 0:
                cost += car.add_charge_i * distance
        else:
            distance -= car.base_d_o
            cost += car.basefare_o
            if distance > 0:
                cost += car.add_charge_o * distance

        if twoway:
            return JsonResponse({"cost": cost * 2, "time": time * 2, "distance": distance * 2})
        else:
            return JsonResponse({"cost": cost , "time": time, "distance": distance })

    return JsonResponse({"error": "Invalid request method"})

