from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.user_management_view, name='user_management'),
    path('categories/', views.category_management_view, name='category_management'),
    path('products/', views.product_management_view, name='product_management'),
    path('add_category/', views.add_category, name='add_category'),

    
]