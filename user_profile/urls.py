from django.urls import path

from . import views

urlpatterns = [
    path("your_profile/", views.user_profile_view, name='your_profile'),
    path("your_orders/", views.your_order, name='your_orders'),
    path("your_addresses/", views.your_addresses, name='your_addresses'),
    path("your_wallet/", views.your_wallet, name='your_wallet'),
    path('order/<uuid:uid>/',views.order_detail, name='order_detail'),
    path('order/<uuid:uid>/return/',views.return_order, name='return_order'),
    path('order/<uuid:uid>/cancel/',views.cancel_order, name='cancel_order'),
]