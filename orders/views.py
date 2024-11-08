from django.shortcuts import render

def checkout(request):
    print("Checkout view hit!")
    return render(request, 'checkout/checkout.html')
