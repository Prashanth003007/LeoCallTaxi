from django.urls import path
from . import views

urlpatterns = [
    path("", views.adminLogin, name="adminlogin"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("logoutpage", views.logoutpage, name="logoutpage"),
    path("contactdev", views.contactdev, name="contactdev"),
    path("bookingdetails",views.bookingdetails,name="bookingdetails"),
    path("week_export",views.emailExportWeek,name="exportweek"),
    path("whole_export",views.emailExportAll,name="exportwhole")
]
