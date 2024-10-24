# views.py
from django.shortcuts import render, get_object_or_404
from .models import products, productImages

def products_catalogue(request, uid):
    product = get_object_or_404(products, uid=uid)
    product_images = product.product_images.all()  # Fetch all images related to the product
    
    return render(request, 'product/product_catalogue.html', {'product': product, 'product_images': product_images})

def add_to_cart(request, uid):
    pass