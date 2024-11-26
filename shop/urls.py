from django.urls import path

from . import views

urlpatterns = [
    path("", views.shop, name='shop'),
    path('filter/', views.filter_shop, name='filter_shop'),
]