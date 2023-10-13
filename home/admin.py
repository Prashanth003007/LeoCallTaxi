from django.contrib import admin
from .models import BookingDetails, JoinDetail, Cars

# Register your models here.

admin.site.register(BookingDetails)
admin.site.register(JoinDetail)
admin.site.register(Cars)
    