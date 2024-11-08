from django.urls import path
from . import views


urlpatterns = [
    path("", views.cart, name='cart'),
    path("update_cart/", views.update_cart, name='update_cart'),
    path("add_to_cart/<uuid:uid>", views.add_to_cart, name='add_to_cart'),
    path("remove_from_cart/", views.remove_from_cart, name='remove_from_cart'),
]