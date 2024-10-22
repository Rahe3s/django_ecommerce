from django.urls import path

from . import views

urlpatterns = [
    path("", views.products_catalogue, name='products_catalogue'),
]