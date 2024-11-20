from django.shortcuts import render,redirect,get_object_or_404
from product.models import ProductVariant,products
from .models import Cart, CartItem
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, F
from decimal import Decimal


def cart(request):
    cart_items = []
    total_price = 0

    try:
        if request.user.is_authenticated:
            # Handle merging session cart into user cart
            session_cart = request.session.get('cart', [])
            if session_cart:
                user_cart, created = Cart.objects.get_or_create(user=request.user)
                
                for item in session_cart:
                    try:
                        # Fetch the product variant based on the session item data
                        product_variant = ProductVariant.objects.filter(uid=item['product_variant_id']).first()
                        
                        if product_variant:
                            cart_item, created = CartItem.objects.get_or_create(
                                cart=user_cart,
                                product_variant=product_variant,
                                defaults={'quantity': item['quantity']}
                            )
                            if not created:
                                cart_item.quantity += item['quantity']
                                cart_item.save()
                    except Exception as e:
                        messages.error(request, f"Error adding item {item['product_variant_id']} to your cart: {e}")
                
                # Clear the session cart after merging
                del request.session['cart']

            # Fetch user's cart items from the database
            user_cart_items = CartItem.objects.filter(cart__user=request.user)
            
            for item in user_cart_items:
                try:
                    product_variant = item.product_variant
                    product = product_variant.product
                    product_images = product.product_images.all()  # Adjust based on image fetching logic
                    
                    cart_items.append({
                        'id': item.id,
                        'variant': product_variant,
                        'product': product,
                        'images': product_images,
                        'quantity': item.quantity,
                        'total_price': product_variant.product.price * item.quantity
                    })
                except Exception as e:
                    messages.error(request, f"Error fetching item {item.id}: {e}")

        else:
            # Handle guest cart
            session_cart = request.session.get('cart', [])
            
            for item in session_cart:
                try:
                    product_variant = ProductVariant.objects.filter(uid=item['product_variant_id']).first()
                    if product_variant:
                        product = product_variant.product
                        product_images = product.product_images.all()  # Adjust based on image fetching logic
                        
                        cart_items.append({
                            'id': item['id'],
                            'variant': product_variant,
                            'product': product,
                            'images': product_images,
                            'quantity': item['quantity'],
                            'total_price': product_variant.product.price * item['quantity']
                        })
                except Exception as e:
                    messages.error(request, f"Error fetching session cart item {item['product_variant_id']}: {e}")

        # Calculate the grand total price
        total_price = sum(item['total_price'] for item in cart_items)

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})
  

def add_to_cart(request, uid):
    if request.method == 'POST':
        try:
            # Retrieve size, color, and quantity from the request
            size = request.POST.get('size')
            color = request.POST.get('color')
            quantity = int(request.POST.get('quantity', 1))

            # Fetch the product and its variant
            try:
                product = get_object_or_404(products, uid=uid)
                product_variant = get_object_or_404(ProductVariant, product=product, size=size, color=color)
            except Exception as e:
                messages.error(request, f"Product or variant not found: {e}")
                return redirect('product_catalogue', uid=uid)

            if request.user.is_authenticated:
                # Ensure the user has a cart
                try:
                    cart, created = Cart.objects.get_or_create(user=request.user)
                except Exception as e:
                    messages.error(request, f"Error creating or retrieving cart: {e}")
                    return redirect('product_catalogue', uid=uid)
                
                # Add the item to the cart
                try:
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart,
                        product_variant=product_variant,
                        defaults={'quantity': quantity}
                    )

                    if not created:
                        # Update the quantity if the item already exists
                        cart_item.quantity += quantity
                        cart_item.save()

                    messages.success(request, "Product added to your cart.")
                except Exception as e:
                    messages.error(request, f"Error adding product to cart: {e}")
                    return redirect('product_catalogue', uid=uid)

                # Clear the session cart if the user is authenticated
                try:
                    if 'cart' in request.session:
                        del request.session['cart']
                except Exception as e:
                    messages.warning(request, f"Could not clear session cart: {e}")

            else:
                # Guest user logic
                try:
                    cart = request.session.get('cart', [])
                    product_exist = False

                    for item in cart:
                        if item['product_variant_id'] == str(product_variant.uid):
                            item['quantity'] += quantity
                            product_exist = True
                            break

                    if not product_exist:
                        cart_item = {
                            'product_variant_id': str(product_variant.uid),
                            'quantity': quantity,
                            'price': product_variant.product.price,
                            'id': str(len(cart))  # Use the length of the cart as a unique ID
                        }
                        cart.append(cart_item)

                    request.session['cart'] = cart
                    request.session.modified = True
                    messages.success(request, "Product added to your session cart.")
                except Exception as e:
                    messages.error(request, f"Error handling guest cart: {e}")
                    return redirect('product_catalogue', uid=uid)

            return redirect('cart')

        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect('product_catalogue', uid=uid)

    return redirect('product_catalogue', uid=uid)
  

    


def update_cart(request):
    if request.method == 'POST':
        try:
            item_id = request.POST.get('item_id')
            new_quantity = int(request.POST.get('new_quantity'))

            if request.user.is_authenticated:
                try:
                    # Debug: Log the received item_id and user
                    print(f"Updating cart item - User: {request.user}, Item ID: {item_id}")

                    # Fetch cart and item
                    cart, created = Cart.objects.get_or_create(user=request.user)
                    cart_item = CartItem.objects.get(cart=cart, id=item_id)  # Only get, don't create

                    # Update quantity
                    cart_item.quantity = new_quantity
                    cart_item.save()

                    # Calculate updated item total
                    item_total = Decimal(cart_item.quantity) * Decimal(cart_item.product_variant.product.price)

                    # Calculate updated total price for the entire cart
                    cart_total = cart.items.aggregate(
                        total=Sum(F('quantity') * F('product_variant__product__price'))
                    )['total'] or 0

                    messages.success(request, "Cart item updated successfully.")
                    return JsonResponse({
                        'success': True,
                        'item_total': float(item_total),
                        'cart_total': float(cart_total),
                    })

                except CartItem.DoesNotExist:
                    messages.error(request, "Cart item not found.")
                    return JsonResponse({'success': False, 'message': 'Cart item not found.'})
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")
                    return JsonResponse({'success': False, 'message': str(e)})

            else:
                try:
                    # Guest user logic
                    cart = request.session.get('cart', [])
                    cart_item = None

                    # Find the item in the session cart
                    for item in cart:
                        if item['id'] == item_id:
                            item['quantity'] = new_quantity
                            cart_item = item
                            break

                    # Check if the item was found and update session
                    if cart_item:
                        request.session['cart'] = cart
                        request.session.modified = True

                        # Calculate item total and cart total
                        item_total = cart_item['quantity'] * cart_item['price']
                        cart_total = sum(item['quantity'] * item['price'] for item in cart)

                        messages.success(request, "Session cart item updated successfully.")
                        return JsonResponse({
                            'success': True,
                            'cart_total': cart_total,
                            'item_total': item_total
                        })
                    else:
                        messages.error(request, "Cart item not found in session cart.")
                        return JsonResponse({'success': False, 'message': 'Cart item not found in session cart.'})
                except Exception as e:
                    messages.error(request, f"An error occurred while updating the session cart: {e}")
                    return JsonResponse({'success': False, 'message': str(e)})

        except ValueError:
            messages.error(request, "Invalid quantity provided.")
            return JsonResponse({'success': False, 'message': 'Invalid quantity.'})
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return JsonResponse({'success': False, 'message': str(e)})
        
        

    messages.error(request, "Invalid request method.")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})






def remove_from_cart(request):
    if request.method == 'POST':
        try:
            item_id = request.POST.get('item_id')

            if request.user.is_authenticated:
                try:
                    cart, created = Cart.objects.get_or_create(user=request.user)
                    cart_item = CartItem.objects.get(cart=cart, id=item_id)

                    # Delete the cart item
                    cart_item.delete()

                    # Calculate updated total price for the entire cart
                    cart_total = cart.items.aggregate(
                        total=Sum(F('quantity') * F('product_variant__product__price'))
                    )['total'] or 0

                    messages.success(request, "Item removed from your cart.")
                    return JsonResponse({
                        'success': True,
                        'cart_total': float(cart_total),
                    })

                except CartItem.DoesNotExist:
                    messages.error(request, "Item not found in your cart.")
                    return JsonResponse({'success': False, 'message': 'Item not found in cart.'})

                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")
                    return JsonResponse({'success': False, 'message': str(e)})

            else:
                try:
                    # For guest user: remove item from session cart
                    cart = request.session.get('cart', [])
                    updated_cart = [item for item in cart if item['id'] != item_id]

                    if len(cart) != len(updated_cart):
                        request.session['cart'] = updated_cart
                        request.session.modified = True

                        # Calculate updated cart total
                        cart_total = sum(item['quantity'] * item['price'] for item in updated_cart)

                        messages.success(request, "Item removed from your session cart.")
                        return JsonResponse({
                            'success': True,
                            'cart_total': cart_total
                        })
                    else:
                        messages.error(request, "Item not found in session cart.")
                        return JsonResponse({'success': False, 'message': 'Item not found in session cart.'})

                except Exception as e:
                    messages.error(request, f"An error occurred while removing the item: {e}")
                    return JsonResponse({'success': False, 'message': str(e)})

        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return JsonResponse({'success': False, 'message': str(e)})

    messages.error(request, "Invalid request method.")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
