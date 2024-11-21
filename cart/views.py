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
        item_id = request.POST.get('item_id')
        new_quantity = request.POST.get('new_quantity')

        if not item_id or not new_quantity.isdigit():
            return JsonResponse({'success': False, 'message': 'Invalid data provided.'}, status=400)

        new_quantity = int(new_quantity)

        if request.user.is_authenticated:
            try:
                # Get the user's cart and the specific cart item
                cart = Cart.objects.get(user=request.user)
                cart_item = CartItem.objects.get(cart=cart, id=item_id)

                # Update the quantity
                cart_item.quantity = new_quantity
                cart_item.save()

                # Calculate totals
                item_total = Decimal(cart_item.quantity) * Decimal(cart_item.product_variant.product.price)
                cart_total = cart.items.aggregate(
                    total=Sum(F('quantity') * F('product_variant__product__price'))
                )['total'] or 0

                return JsonResponse({
                    'success': True,
                    'item_total': float(item_total),
                    'cart_total': float(cart_total),
                })

            except CartItem.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Item not found in cart.'}, status=404)

        else:
            # Handle session-based cart
            cart = request.session.get('cart', [])
            for item in cart:
                if str(item['id']) == item_id:
                    item['quantity'] = new_quantity
                    request.session.modified = True

                    item_total = item['quantity'] * item['price']
                    cart_total = sum(i['quantity'] * i['price'] for i in cart)

                    return JsonResponse({
                        'success': True,
                        'item_total': item_total,
                        'cart_total': cart_total,
                    })

            return JsonResponse({'success': False, 'message': 'Item not found in session cart.'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                cart_item = CartItem.objects.get(cart=cart, id=item_id)
                cart_item.delete()

                cart_total = cart.items.aggregate(
                    total=Sum(F('quantity') * F('product_variant__product__price'))
                )['total'] or 0

                return JsonResponse({'success': True, 'cart_total': float(cart_total)})

            except CartItem.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Item not found in cart.'}, status=404)

        else:
            cart = request.session.get('cart', [])
            updated_cart = [item for item in cart if str(item['id']) != item_id]

            if len(updated_cart) != len(cart):
                request.session['cart'] = updated_cart
                request.session.modified = True

                cart_total = sum(item['quantity'] * item['price'] for item in updated_cart)
                return JsonResponse({'success': True, 'cart_total': cart_total})

            return JsonResponse({'success': False, 'message': 'Item not found in session cart.'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)