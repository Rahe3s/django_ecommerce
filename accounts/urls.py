
from django.urls import path

from . import views

urlpatterns = [
    path("registration", views.registration, name='registration'),
    path("login", views.login_page, name='login_page'),
    path("logout", views.logout_page, name='logout_page'),
    path("otp_verification", views.otp_verification, name='otp_verification'),
]