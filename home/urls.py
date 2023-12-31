from django.urls import path
from . import views

urlpatterns = [
    path("", views.userHome, name="user_home"),
    path("book", views.book, name="book"),
    path("prebook",views.prebook,name="prebook"),
    path("book2", views.book2, name="book2"),
    path("booked", views.booked, name="booked"),
    path("booked2", views.booked2, name="booked"),
    path("about", views.about, name="about"),
    path("joinus",views.joinus,name="joinus"),
    path("home",views.userHome,name="user-home"),
    path("join",views.join,name="join"),
    path("verify",views.verify,name="verify"),
    path("calculate_price",views.calculate_price,name="calculate_price")
]
