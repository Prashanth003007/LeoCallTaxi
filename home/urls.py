from django.urls import path
from . import views

urlpatterns = [
    path("", views.userHome, name="user_home"),
    path("book", views.book, name="book"),
    path("booked", views.booked, name="booked"),
    path("about", views.about, name="about")
]
