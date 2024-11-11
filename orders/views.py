from django.shortcuts import render,redirect
from .models import Coupons,Address
from cart.models import CartItem,Cart
from django.http import JsonResponse
from .forms import AddressForm
from django.contrib import messages


def checkout(request):
    # Retrieve or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.product_variant.product.price * item.quantity for item in cart_items)

    # Get available coupons based on the cart total
    available_coupons = Coupons.objects.filter(min_amount__lte=cart_total)

    # Retrieve the user's saved addresses
    addresses = Address.objects.filter(user=request.user)
    form = AddressForm()


    # Pass all necessary data to the template
    return render(request, 'checkout/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'available_coupons': available_coupons,
        'addresses': addresses,
        'form': form,
    })

from django.http import JsonResponse
from .models import Address
from .forms import AddressForm

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            # Fetch updated list of addresses
            addresses = Address.objects.filter(user=request.user).values(
                'name', 'address', 'place', 'state', 'PIN'
            )
            return JsonResponse({'success': True, 'addresses': list(addresses)})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def apply_coupon(request):
    if request.method == 'POST':
        coupon_uid = request.POST.get('coupon_uid')
        print(coupon_uid)
        
        cart_total = request.session.get('cart_total', 0)
        print(cart_total)  # Fetch or calculate cart total as needed

        try:
            # Check if coupon exists and meets the min_amount requirement
            coupon = Coupons.objects.get(uid=coupon_uid)
            print('coupon found')
            cart_total = float(request.POST.get('cart_total'))
            discount = coupon.discount # Example discount calculation, adjust as needed

            # Calculate the new order total
            order_total = cart_total - discount

            return JsonResponse({
                'success': True,
                'discount': discount,
                'order_total': order_total
            })

        except Coupons.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid or ineligible coupon selected.'
            })

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})