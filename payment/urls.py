from django.urls import path

from . import views



urlpatterns = [
    path("place_order/", views.place_order, name='place_order'),
    path("payment/", views.payment_page, name='payment_page'),
    path("success/", views.success_page, name='success_page'),

]