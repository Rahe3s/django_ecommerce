from django.shortcuts import render
from product.models import products

def shop(request):
    products_list = products.objects.prefetch_related('product_images').all()
    return render(request, 'shop/shop.html', {'products_list': products_list})
    