from django.urls import path

from . import views



urlpatterns = [
    path("place_order/", views.place_order, name='place_order'),
    path("payment/", views.payment_page, name='payment_page'),
    path('payment/', views.payment_page, name='payment_page'), 
    path('payment/success/', views.payment_success, name='payment_success'),
    path("success/<uuid:uid>", views.success_page, name='success_page'),

]