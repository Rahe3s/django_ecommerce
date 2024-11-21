from django.shortcuts import render
from .models import Banner

def home(request):
    banner = Banner.objects.first()
    return render(request, 'home/home.html',{'banner':banner})


def contact(request):
    return render(request, 'home/contact.html')



def about(request):
    return render(request, 'home/about.html')