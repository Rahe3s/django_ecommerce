from django.shortcuts import render,redirect
from .models import Coupons,Address
from cart.models import CartItem,Cart
from django.http import JsonResponse
from .forms import AddressForm
from django.template.loader import render_to_string

from django.contrib import messages



def checkout(request):
    # Retrieve or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.product_variant.product.price * item.quantity for item in cart_items)

    # Get available coupons based on the cart total
    available_coupons = Coupons.objects.filter(min_amount__lte=cart_total)

    # Retrieve the user's saved addresses
    addresses = Address.objects.filter(user=request.user).order_by('-created_at')[:3]
    form = AddressForm()


    # Pass all necessary data to the template
    return render(request, 'checkout/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'available_coupons': available_coupons,
        'addresses': addresses,
        'form': form,
    })


def add_address(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = AddressForm(request.POST)
        
        if form.is_valid():
            # Save the new address and link it to the user
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            # Retrieve the updated address list
            addresses = Address.objects.filter(user=request.user).order_by('-created_at')[:3]

            # Render the updated address list as HTML
            address_list_html = render_to_string('checkout/address_list_partial.html', {'addresses': addresses})

            # Return success response with the rendered HTML
            return JsonResponse({'success': True, 'address_list_html': address_list_html})
        
        else:
            # Return form errors if form is invalid
            return JsonResponse({'success': False, 'errors': form.errors})
    
    # Return an error if request is not POST or user is not authenticated
    return JsonResponse({'success': False, 'errors': 'Invalid request.'})

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