from django.db import models

VEHICLE_CHOICES = (
    ("INA", "INA"),
    ("SE", "SEDAN"),
    ("MU", "MUV"),
    ("MP", "MUV PRIME"),
    ("SV", "SUV"),
    ("TP", "TEMPO"),
)



# Create your models here.

class Cars(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=3)
    basefare_o = models.SmallIntegerField()
    basefare_i = models.SmallIntegerField()
    add_charge_o = models.SmallIntegerField()
    add_charge_i = models.SmallIntegerField()
    base_d_i = models.SmallIntegerField()
    base_d_o = models.SmallIntegerField()

class JoinDetail(models.Model):
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    reqdate = models.DateField(auto_now_add=True)

class BookingDetails(models.Model):
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=10)
    pickupdate = models.DateField()
    pickuptime = models.TimeField()
    pickup = models.TextField()
    dropoff = models.TextField()
    ride = models.CharField(max_length=3)
    twoway = models.BooleanField(default=False)
    bookingdate = models.DateField(auto_now_add=True)
    email = models.EmailField()
    efare = models.IntegerField()
    verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)
