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
            product_variant = ProductVariant.objects.filter(uid=item['product_variant_id']).first()
            if product_variant:
                product = product_variant.product
                product_images = product.product_images.all()  # Assuming this is how you fetch product images
                
                cart_items.append({
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
        
        return redirect('cart')
    return redirect('product_catalogue', uid=uid)  

  


    


def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = request.POST.get('new_quantity')

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
            for cart_items in cart:
                if cart_items['id'] == item_id:  # Match the ID to find the item
                    cart_items['quantity'] = new_quantity
                    print('1')
                    break
            request.session['cart'] = cart
            request.session.modified = True

            # Calculate total price for guest cart
            total_price = sum(item['quantity'] * item['price'] for item in cart)

            return JsonResponse({
                'success': True,
                'new_quantity': new_quantity,
                'cart_total': total_price,
                'item_total': cart_items['quantity'] * cart_items['price'],  # Calculate the item total
            })

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




def remove_from_cart(request, uid):
    product_variant = get_object_or_404(ProductVariant, uid=uid)

    if request.user.is_authenticated:
        # Remove the item from the authenticated user's database cart
        cart_item = CartItem.objects.filter(cart__user=request.user, product_variant=product_variant).first()
        
        if cart_item:
            cart_item.delete()
            messages.success(request, "Item removed from your cart.")
            success = True
        else:
            messages.error(request, "Item not found in your cart.")
            success = False

    else:
        # For guest users, update the cart stored in the session
        cart = request.session.get('cart', [])
        cart = [item for item in cart if item['variant'] != str(product_variant.uid)]
        request.session['cart'] = cart
        request.session.modified = True  # Save session changes
        messages.success(request, "Item removed from your session cart.")
        success = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Return a JSON response for AJAX requests
        return JsonResponse({'success': success})

    return redirect('cart')

