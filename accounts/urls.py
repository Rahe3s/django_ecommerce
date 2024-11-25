
from django.urls import path

from . import views

urlpatterns = [
    path("registration", views.registration, name='registration'),
    path("login", views.login_page, name='login_page'),
    path("logout", views.logout_page, name='logout_page'),
    path("otp_verification", views.otp_verification, name='otp_verification'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
]