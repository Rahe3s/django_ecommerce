from django.urls import path

from . import views

urlpatterns = [
    path("", views.products_catalogue, name='product_catalogue'),
    path("", views.products_catalogue, name='add_to_cart'),
    

]