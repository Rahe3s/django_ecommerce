from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.db.models import Sum
from .models import products

def products_catalogue(request, uid):
    try:
        # Fetch the product by its unique ID (uid)
        product = get_object_or_404(products, uid=uid)

        # Fetch all images related to the product
        product_images = product.product_images.all()

        # Fetch all variants related to the product
        product_variants = product.variants.all()

        # Check total stock across all variants
        total_stock = product_variants.aggregate(total_stock=Sum('stock'))['total_stock'] or 0

        # Fetch unique sizes and colors if stock is available
        unique_sizes = []
        unique_colors = []
        if total_stock > 0:
            unique_sizes = product_variants.values_list('size', flat=True).distinct()
            unique_colors = product_variants.values_list('color', flat=True).distinct()

        return render(request, 'product/product_catalogue.html', {
            'product': product,
            'product_images': product_images,
            'product_variants': product_variants,
            'unique_sizes': unique_sizes,
            'unique_colors': unique_colors,
            'is_in_stock': total_stock > 0,  # Check if the product is in stock
        })

    except Http404:
        # Handle the case where the product is not found
        messages.error(request, "The product you are looking for does not exist.")
        return redirect('shop')  # Replace 'shop' with the name of your shop page URL pattern

    except Exception as e:
        # Log the exception (optional, replace with logging module in production)
        print(f"Error in products_catalogue view: {e}")

        # Add a general error message and redirect to the shop page
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return redirect('shop')  # Replace 'shop' with the name of your shop page URL pattern
