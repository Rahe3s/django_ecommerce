from django.urls import path

from . import views



urlpatterns = [
    path("", views.checkout, name='checkout'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('add_address/', views.add_address, name='add_address'),
]