from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from orders.models import Coupons,Address
from django.http import JsonResponse
import uuid





def place_order(request):
    if request.method == 'POST':
        try:
            # Fetch cart and cart items for the user
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_total = sum(item.product_variant.product.price * item.quantity for item in cart_items)

            # Get selected address, payment method, and coupon
            address_id = request.POST.get('selected_address')
            payment_method = request.POST.get('payment_method')  # COD, Stripe, etc.
            coupon_id = request.POST.get('coupon')

            # Log the received data for debugging
            print('Selected Address ID:', address_id)
            print('Selected Payment Method:', payment_method)
            print('Selected Coupon:', coupon_id)

            # Validate address
            try:
                address = Address.objects.get(uid=address_id)
            except Address.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid address selected.'}, status=400)

            # Validate coupon (if provided)
            discount_amount = 0
            if coupon_id:
                try:
                    coupon = Coupons.objects.get(uid=coupon_id)
                    if cart_total >= coupon.min_amount:
                        discount_amount = coupon.discount
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Coupon does not meet the cart total requirement.'}, status=400)
                except Coupons.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Invalid coupon provided.'}, status=400)

            # Calculate the final order total
            order_total = max(cart_total - discount_amount, 0)

            # Handle Cash on Delivery (COD)
            if payment_method == 'COD':
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    uid=uuid.uuid4(),
                    address=address,
                    cart_total=cart_total,
                    final_amount=order_total,
                    discount_amount=discount_amount,
                    payment_method='COD',
                    payment_status='Pending'  # Initial status for COD
                )

                # Create order items
                for item in cart_items:
                    OrderItem.objects.create(
                        uid=uuid.uuid4(),
                        order=order,
                        product_variant=item.product_variant,
                        quantity=item.quantity,
                        price=item.product_variant.product.price
                    )

                # Clear the cart after successful order placement
                cart_items.delete()

                # Respond with a success message
                return JsonResponse({'status': 'success', 'order_id': str(order.uid)})

            # Handle other payment methods (e.g., Stripe)
            else:
                # Save order data in session for payment processing
                request.session['order_data'] = {
                    'address_id': address_id,
                    'order_total': order_total,
                    'discount': discount_amount,
                    'cart_total': cart_total
                }

                # Redirect to the payment page (e.g., Stripe)
                return JsonResponse({'status': 'redirect', 'url': reverse('payment_page')})

        except Exception as e:
            # Log unexpected errors
            print("Error in place_order:", str(e))
            return JsonResponse({'status': 'error', 'message': 'Something went wrong. Please try again.'}, status=500)

    # Redirect to the checkout page if the request is not POST
    return redirect('checkout')



def payment_page(request):
    return render(request,'payment/payment.html')


from django.shortcuts import render
from datetime import datetime

def success_page(request, uid):
    # Fetch order details
    try:
        order = Order.objects.get(uid=uid)
        order_items = OrderItem.objects.filter(order=order)
        context = {
            'order_id': order.uid,
            'order_total_items': order_items.count(),
            'cart_total': order.cart_total,
            'discount_amount': order.discount_amount,
            'final_amount': order.final_amount,
            'payment_method': order.payment_method,
            'year': datetime.now().year,
        }
        return render(request, 'payment/success.html', context)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('home')
