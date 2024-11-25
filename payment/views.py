from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from orders.models import Coupons,Address
from django.http import JsonResponse
import uuid
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from datetime import datetime


stripe.api_key = settings.STRIPE_SECRET_KEY



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
                    'cart_total': cart_total,
                    'coupon_id':coupon_id,
                    'cart_uid': str(cart.uid),
                }

                # Redirect to the payment page (e.g., Stripe)
                return JsonResponse({'status': 'redirect', 'url': reverse('payment_page')})

        except Exception as e:
            # Log unexpected errors
            print("Error in place_order:", str(e))
            return JsonResponse({'status': 'error', 'message': 'Something went wrong. Please try again.'}, status=500)

    # Redirect to the checkout page if the request is not POST
    return redirect('checkout')



@login_required
def payment_page(request):
    order_data = request.session.get('order_data', None)
    if order_data:
        try:
            # Create Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(order_data['order_total'] * 100),  # Amount in cents
                currency='usd',
                payment_method_types=['card'],
                metadata={
                    'order_uid': str(uuid.uuid4())  # Use a unique identifier for the order
                }
            )
            context = {
                'client_secret': intent['client_secret'],
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
                'order_total': order_data['order_total']
            }
            return render(request, 'payment/payment.html', context)
        except Exception as e:
            messages.error(request, f'Error creating payment intent: {str(e)}')
            return redirect('checkout')
    return redirect('checkout')

@login_required
def payment_success(request):
    order_data = request.session.get('order_data', None)
    if order_data:
        try:
            # Fetch cart items using cart_uid
            cart = Cart.objects.get(uid=order_data['cart_uid'])
            cart_items = CartItem.objects.filter(cart=cart)

            # Validate address
            address = Address.objects.get(uid=order_data['address_id'])
            
            # Validate coupon (if provided)
            discount_amount = order_data['discount']
            coupon = None
            if order_data['coupon_id']:
                coupon = Coupons.objects.get(uid=order_data['coupon_id'])

            # Create the order
            order = Order.objects.create(
                user=request.user,
                uid=uuid.uuid4(),
                address=address,
                cart_total=order_data['cart_total'],
                final_amount=order_data['order_total'],
                discount_amount=discount_amount,
                payment_method='credit_card',
                payment_status='paid'
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

            # Clear the cart
            cart_items.delete()

            # Return success response with order_uid
            return JsonResponse({'status': 'success', 'order_uid': str(order.uid)})
        
        except Exception as e:
            print("Error creating order:", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Order data not found in session.'}, status=400)


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

@login_required
def payment_cancel(request):
    messages.info(request, 'Your payment has been cancelled.')
    return render(request, 'payment/cancel.html')

