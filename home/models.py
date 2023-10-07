from django.db import models

VEHICLE_CHOICES = (
    ("MI", "MINI"),
    ("SE", "SEDAN"),
    ("MU", "MUV"),
    ("MP", "MUV PRIME"),
    ("SV", "SUV"),
    ("TP", "TEMPO"),
)


# Create your models here.
class BookingDetails(models.Model):
    name = models.CharField(max_length=70)
    phone = models.CharField(max_length=10)
    pickupdate = models.DateField()
    pickuptime = models.TimeField()
    pickup = models.TextField()
    dropoff = models.TextField()
    ride = models.CharField(
        max_length=2,
        choices=VEHICLE_CHOICES,
        default=VEHICLE_CHOICES[0][0]
    )
    twoway = models.BooleanField(default=False)
    bookingdate = models.DateField(auto_now_add=True)
