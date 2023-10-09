from django.urls import path
from . import views

urlpatterns = [
    path("", views.userHome, name="user_home"),
    path("book", views.book, name="book"),
    path("booked", views.booked, name="booked"),
    path("about", views.about, name="about"),
    path("joinus",views.joinus,name="joinus"),
    path("home",views.userHome,name="user-home"),
    path("join",views.join,name="join")
]
