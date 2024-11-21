from django.shortcuts import render,redirect
from .models import Coupons,Address
from cart.models import CartItem,Cart
from django.http import JsonResponse
from .forms import AddressForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def checkout(request):
    if not request.user.is_authenticated:
        # Add a message and redirect to the login page
        messages.info(request, "Please log in to checkout the cart.")
        return redirect('login_page')  # Replace 'login_page' with the correct login view name in your project

    try:
        # Retrieve or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_total = sum(item.product_variant.product.price * item.quantity for item in cart_items)

        # Get available coupons based on the cart total
        available_coupons = Coupons.objects.filter(min_amount__lte=cart_total)

        # Retrieve the user's saved addresses
        addresses = Address.objects.filter(user=request.user).order_by('-created_at')[:3]
        form = AddressForm()

        # Add a checkout process message
        messages.info(request, "Complete your checkout process.")

        # Pass all necessary data to the template
        return render(request, 'checkout/checkout.html', {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'available_coupons': available_coupons,
            'addresses': addresses,
            'form': form,
        })

    except Exception as e:
        # Handle unexpected errors gracefully
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('home')  # Redirect to the home page or another appropriate view
    
def add_address(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            form = AddressForm(request.POST)
            
            if form.is_valid():
                try:
                    # Save the new address and link it to the user
                    address = form.save(commit=False)
                    address.user = request.user
                    address.save()

                    # Retrieve the updated address list
                    addresses = Address.objects.filter(user=request.user).order_by('-created_at')[:3]

                    # Render the updated address list as HTML
                    address_list_html = render_to_string('checkout/address_list_partial.html', {'addresses': addresses})

                    return JsonResponse({
                        'success': True,
                        'message': "Address added successfully.",
                        'address_list_html': address_list_html
                    })

                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'message': f"An error occurred while saving the address: {e}"
                    })

            else:
                # Handle form validation errors
                return JsonResponse({
                    'success': False,
                    'message': "Invalid address details. Please correct the errors and try again.",
                    'errors': form.errors
                })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f"An unexpected error occurred: {e}"
            })

    # Handle invalid request types or unauthenticated users
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': "You need to log in to add an address."})
    else:
        return JsonResponse({'success': False, 'message': "Invalid request method."})



def apply_coupon(request):
    if request.method == 'POST':
        try:
            coupon_uid = request.POST.get('coupon_uid')
            cart_total = float(request.POST.get('cart_total', 0))  # Ensure cart_total is fetched as a float

            # Validate cart total
            if cart_total <= 0:
                return JsonResponse({'success': False, 'message': 'Invalid cart total. Please check your cart.'})

            try:
                # Check if the coupon exists
                coupon = Coupons.objects.get(uid=coupon_uid)

                # Validate coupon conditions
                if cart_total < coupon.min_amount:
                    return JsonResponse({
                        'success': False,
                        'message': f"Coupon requires a minimum cart total of {coupon.min_amount}."
                    })

                # Calculate the discount and order total
                discount = coupon.discount
                order_total = cart_total - discount

                return JsonResponse({
                    'success': True,
                    'message': "Coupon applied successfully.",
                    'discount': discount,
                    'order_total': order_total
                })

            except Coupons.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid or expired coupon.'
                })

        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid cart total format.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f"An unexpected error occurred: {e}"})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

