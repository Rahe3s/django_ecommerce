from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')


def contact(request):
    return render(request, 'home/contact.html')



def about(request):
    return render(request, 'home/about.html')