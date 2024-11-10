from django.shortcuts import render
from .models import Coupons
from cart.models import CartItem,Cart
from django.http import JsonResponse

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(item.product_variant.product.price*item.quantity for item in cart_items)
    available_coupons = Coupons.objects.filter(min_amount__lte=cart_total)
    

    return render(request, 'checkout/checkout.html', {
        'cart_items':cart_items,
        'cart_total': cart_total,
        'available_coupons':available_coupons
    })

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