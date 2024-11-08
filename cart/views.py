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

    if request.user.is_authenticated:
        # Check if there's a session cart with items and add them to the user's cart
        session_cart = request.session.get('cart', [])
        if session_cart:
            # Get or create a cart for the authenticated user
            user_cart, created = Cart.objects.get_or_create(user=request.user)

            for item in session_cart:
                # Fetch the product variant based on the session item data
                product_variant = ProductVariant.objects.filter(uid=item['product_variant_id']).first()
                
                if product_variant:
                    # Add each session cart item to the authenticated user's cart in the database
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=user_cart,
                        product_variant=product_variant,
                        defaults={'quantity': item['quantity']}
                    )
                    if not created:
                        cart_item.quantity += item['quantity']
                        cart_item.save()

            # Clear the session cart after merging
            del request.session['cart']

        # Fetch user's cart items from the database
        user_cart_items = CartItem.objects.filter(cart__user=request.user)
        
        for item in user_cart_items:
            product_variant = item.product_variant
            product = product_variant.product
            product_images = product.product_images.all()
            
              # Adjust based on image fetching logic
            
            cart_items.append({
                'id': item.id,
                'variant': product_variant,
                'product': product,
                'images': product_images,
                'quantity': item.quantity,
                'total_price': product_variant.product.price * item.quantity  # Total price per item
            })

    else:
        # Fetch cart items from session for guests
        cart = request.session.get('cart', [])
        
        
        
        for item in cart:
            print('iti',item['id'])
            product_variant = ProductVariant.objects.filter(uid=item['product_variant_id']).first()
            if product_variant:
                product = product_variant.product
                product_images = product.product_images.all()  # Assuming this is how you fetch product images
                
                cart_items.append({
                    'id': item['id'],
                    'variant': product_variant,
                    'product': product,
                    'images': product_images,
                    'quantity': item['quantity'],
                    'total_price': product_variant.product.price * item['quantity']  # Calculate total price for each item
                })

    # Calculate the grand total price from all items in the cart
    total_price = sum(item['total_price'] for item in cart_items)

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

  

def add_to_cart(request, uid):
    if request.method == 'POST':
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(products, uid=uid)
        product_variant = get_object_or_404(ProductVariant, product=product, size=size, color=color)

        if request.user.is_authenticated:
            # Ensure the user has a cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Add the item to the cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_variant=product_variant,
                defaults={'quantity': quantity}
            )

            if not created:
                # If the item already exists, update the quantity
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, "Product added to your cart.")
            
            # Clear the session cart if the user is authenticated
            if 'cart' in request.session:
                del request.session['cart']  # Remove the session cart

        else:
            # Guest user logic
            cart = request.session.get('cart', [])
            product_exist = False

            for item in cart:
                if item['product_variant_id'] == str(product_variant.uid):
                    print('iti',item['id'])
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
                print(cart_item['id'])
                cart.append(cart_item)

            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, "Product added to your session cart.")
        
        return redirect('cart')
    return redirect('product_catalogue', uid=uid)  

  

    


def update_cart(request):
    if request.method == 'POST':
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
                item_total = Decimal(cart_item.quantity) * Decimal(cart_item.product_variant.product.price)
                print(item_total)


                # Calculate updated total price for the entire cart
                cart_total = cart.items.aggregate(
                    total=Sum(F('quantity') * F('product_variant__product__price'))
                )['total']


                return JsonResponse({
                    'success': True,
                    'item_total': float(item_total),  # Ensure it's a float or Decimal
                    'cart_total': float(cart_total), 
                })

            except CartItem.DoesNotExist:
                # Debug: Log if item not found
                print(f"Cart item with ID {item_id} not found for user {request.user}")
                return JsonResponse({'success': False, 'message': 'Cart item not found.'})

            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

        else:
    # Guest user logic
            
            cart = request.session.get('cart', [])
             # Initialize cart_item to None
            
    # Loop through the cart to find the item and update its quantity
            for cart_item in cart:
                print('cart_item id',cart_item['id'] )
                print('item_id',item_id)
                if cart_item['id'] == item_id:  # Match the ID to find the item
                    cart_item['quantity'] = new_quantity
                    
                     # Set cart_item to the found item for later use
                    break

    # Check if the item was found and update session
            if cart_item:
                request.session['cart'] = cart
                request.session.modified = True

        # Calculate item total and cart total
                print('quanr',new_quantity)
                print(cart_item['quantity'])
                print(f"Updating cart item - User: {Cart.uid}, Item ID: {item_id}")
                item_total = cart_item['quantity'] * cart_item['price']
                cart_total = sum(item['quantity'] * item['price'] for item in cart)

                print(f"Debug - Updated quantity for cart item: {cart_item['quantity']}")

                print(f"Debug - Calculated item_total: {item_total}")
                print(f"Debug - Calculated cart_total: {cart_total}")

                return JsonResponse({
                    'success': True,
                    'cart_total': cart_total,
                    'item_total': item_total
                })
            else:
                return JsonResponse({'success': False, 'message': 'Cart item not found in session cart.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})






def remove_from_cart(request):
    if request.method == 'POST':
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

                return JsonResponse({
                    'success': True,
                    'cart_total': float(cart_total),
                })

            except CartItem.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Item not found in cart.'})

        else:
            # For guest user: remove item from session cart
            cart = request.session.get('cart', [])
            updated_cart = [item for item in cart if item['id'] != item_id]

            if len(cart) != len(updated_cart):
                request.session['cart'] = updated_cart
                request.session.modified = True

                cart_total = sum(item['quantity'] * item['price'] for item in updated_cart)

                return JsonResponse({
                    'success': True,
                    'cart_total': cart_total
                })
            else:
                return JsonResponse({'success': False, 'message': 'Item not found in session cart.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
