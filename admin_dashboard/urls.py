from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.user_management_view, name='user_management'),
    path('user/<uuid:uid>/block/', views.block_user, name='block_user'),
    path('user/<uuid:uid>/unblock/', views.unblock_user, name='unblock_user'),
    path('categories/', views.category_management_view, name='category_management'),
    path('products/', views.product_management_view, name='product_management'),
    path('add_category/', views.add_category, name='add_category'),
    path('categories/update/<uuid:uid>/', views.update_category, name='update_category'),
    path('categories/delete/<uuid:uid>/', views.delete_category, name='delete_category'),
    path('add_product/', views.add_product, name='add_product'),
    path('products/<uuid:uid>/update/', views.update_product, name='update_product'),
    path('products/<uuid:uid>/delete/', views.delete_product, name='delete_product'),
    path('add-variant/', views.add_product_variant, name='add_product_variant'),
    path('variants/<uuid:uid>/update/', views.update_product_variant, name='update_product_variant'),
    path('variants/<uuid:uid>/delete/', views.delete_product_variant, name='delete_product_variant'),
    path('banner_coupon/', views.banner_coupon_view, name='banner_coupon'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('coupons/<uuid:uid>/update/', views.update_coupon, name='update_coupon'),
    path('coupons/<uuid:uid>/delete/', views.delete_coupon, name='delete_coupon'),
    path('add_banner/', views.add_banner, name='add_banner'),
    path('banner/<uuid:uid>/update/', views.update_banner, name='update_banner'),
    path('banner/<uuid:uid>/delete/', views.delete_banner, name='delete_banner'),
    path('order_management/', views.order_management_view, name='order_management'),
    path('approve-return/<uuid:order_uid>/', views.approve_return, name='approve_return'),
    path('reject-return/<uuid:order_uid>/', views.reject_return, name='reject_return'),


   


    
]