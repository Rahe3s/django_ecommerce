# views.py
from django.shortcuts import render, get_object_or_404
from .models import products, productImages

def products_catalogue(request, uid):
    # Fetch the product by its unique ID (uid)
    product = get_object_or_404(products, uid=uid)
    
    # Fetch all images related to the product
    product_images = product.product_images.all()
    
   
    product_variants = product.variants.all()
    unique_sizes = product_variants.values_list('size', flat=True).distinct()
    unique_colors = product_variants.values_list('color', flat=True).distinct()

    return render(request, 'product/product_catalogue.html', {
        'product': product,
        'product_images': product_images,
        'product_variants':product_variants,
        'unique_sizes': unique_sizes,  # Pass unique sizes to the template
        'unique_colors': unique_colors,  # Pass unique colors to the template
    })


def add_to_cart(request, uid):
    pass