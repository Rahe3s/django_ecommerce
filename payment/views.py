
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from orders.models import Coupons,Address
from orders.forms import AddressForm

def place_order(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_total = sum(item.product_variant.product.price * item.quantity for item in cart_items)

        # Get selected address and payment method
        address_id = request.POST.get('selected_address')
        print('add id',address_id)
        payment_method = request.POST.get('payment_method')  # e.g., "COD" or "Stripe"
        print('pm',payment_method)
        address = Address.objects.get(uid=address_id)
       
        # Fetch discount if a coupon is applied
        coupon_id = request.POST.get('coupon')
        discount_amount = 0
        if coupon_id:
            coupon = Coupons.objects.get(id=coupon_id)
            if cart_total >= coupon.min_amount:
                discount_amount = coupon.discount
        
        # Calculate final total after discount
        order_total = max(cart_total - discount_amount, 0)

        if payment_method == 'COD':
            # Save Order and Order Items for COD
            order = Order.objects.create(
                user=request.user,
                address=address,
                cart_total=cart_total,
                final_amount=order_total,
                discount_amount=discount_amount,
                payment_method='COD',
                payment_status='Pending'  # Set initial status
            )

            # Save Order Items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_variant=item.product_variant,
                    quantity=item.quantity,
                    price=item.product_variant.product.price * item.quantity
                )

            # Clear cart after successful order
            cart_items.delete()
            
            # Redirect to success page with a message
            messages.success(request, "Your order has been placed successfully!")
            return redirect('success_page')

        else:
            # Redirect to Stripe payment page
            request.session['order_data'] = {
                'address_id': address_id,
                'order_total': order_total,
                'discount': discount_amount,
                'cart_total': cart_total
            }
            return redirect(reverse('payment_page'))
    
    # Redirect back if the request is not POST
    return redirect('checkout')


def payment_page(request):
    return render(request,'payement/payment.html')


def success_page(request):
    return render(request,'payment/success.html')
