from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import smtplib, ssl
from email.message import EmailMessage
from random import randint
from . import models
import requests
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token
git

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
def autocomplete(request):
    query = request.GET.get('query')
    suggestions = []

    if query:
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json",
        }
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            suggestions = [result['display_name'] for result in data if 'India' in result['display_name']]

    return JsonResponse(suggestions, safe=False)# this json should be displayed in the dropdown menu in frontend


def place_to_postal_code(place):
    # Initialize the geolocator using Nominatim
    geolocator = Nominatim(user_agent="place_to_postal_code")

    try:
        location = geolocator.geocode(place)
        if location:
            postal_code = location.raw.get('address', {}).get('postcode')
            if postal_code:
                return postal_code
            else:
                return "Postal code not found for this location."
        else:
            return "Location not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_coordinates(postal_code):
    geolocator = Nominatim(user_agent="postal_code_geocoder")
    location = geolocator.geocode(postal_code)

    if location is not None:
        return (location.latitude, location.longitude)
    else:
        return None


def calculate_distance_between_pincodes(place1, place2):
    coordinates1 = get_coordinates(place_to_postal_code(place1))
    coordinates2 = get_coordinates(place_to_postal_code(place2))


    if coordinates1 is None:
        return f"Postal code for {place1} not found"
    elif coordinates2 is None:
        return f"Postal code for {place2} not found"

    distance = geodesic(coordinates1, coordinates2).kilometers
    return distance

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


