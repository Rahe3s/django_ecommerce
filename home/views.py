from django.shortcuts import render
from .models import Banner
from product.models import Category,products
from django.views.decorators.cache import cache_control



def home(request):
    banner = Banner.objects.get(position='homepage')
    categories = Category.objects.all()
    products_list = products.objects.prefetch_related('product_images').order_by('-created_date')[:4]

    return render(request, 'home/home.html',{'banner':banner , 'categories': categories, 'products_list':products_list})


def contact(request):
    banner = Banner.objects.get(position = 'homepage')
    return render(request, 'home/contact.html',{'banner':banner })



def about(request):
    banner = Banner.objects.get(position = 'homepage')
    about_banner = Banner.objects.get(position = 'shoppage')
    return render(request, 'home/about.html',{'banner':banner, 'about_banner': about_banner })