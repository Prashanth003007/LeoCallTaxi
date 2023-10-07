from django.urls import path
from . import views

urlpatterns = [
    path("", views.adminLogin, name="adminlogin"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("contactedev", views.contactdev, name="contactdev")
]
