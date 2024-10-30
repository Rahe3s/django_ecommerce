from django.shortcuts import render,redirect,get_object_or_404
from product.models import ProductVariant,products
from .models import Cart, CartItem
from django.contrib import messages

def cart(request):
    cart_items = []
    total_price = 0

    if request.user.is_authenticated:
        # Fetch cart items from the database for logged-in users
        user_cart_items = CartItem.objects.filter(user=request.user)  # Adjust as per your CartItem model structure
        
        for item in user_cart_items:
            product_variant = item.variant  # Assuming CartItem has a ForeignKey to ProductVariant
            product = product_variant.product
            product_images = product.product_images.all()  # Assuming this is how you fetch product images
            
            cart_items.append({
                'variant': product_variant,
                'product': product,
                'images': product_images,
                'quantity': item.quantity,
                'total_price': product_variant.product.price * item.quantity  # Calculate total price for each item
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

  

def add_to_cart(request,uid):
    if request.method == 'POST':
        print("entered")
        size = request.POST.get('size')
        color = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))


        product = get_object_or_404(products, uid=uid)
        product_variant = get_object_or_404(ProductVariant, product=product, size=size, color=color)

        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user = request.user,
                variant = product_variant,
                defaults= {'quantity': quantity},
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            messages.success(request, "Product added to your cart.")
        else:
#             # Logic to add the product to session
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
                    'quantity': quantity

                }

                cart.append(cart_item)  # Add item to the cart list in session
            request.session['cart'] = cart 
            messages.success(request, "Product added to your session cart.")
            print("success")
        return redirect('cart') 

    return redirect('product_catalogue', uid=uid)  

# def add_to_cart(request,uid):
#     if request.method == 'POST':
#         print('entered to cart')
    

    

def update_cart(request):
    pass

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem, ProductVariant

def remove_from_cart(request, uid):
    # Fetch the product variant to remove based on the provided uid
    product_variant = get_object_or_404(ProductVariant, uid=uid)

    if request.user.is_authenticated:
        # If the user is authenticated, try to remove the item from the database cart
        cart_item = CartItem.objects.filter(user=request.user, variant=product_variant).first()
        if cart_item:
            cart_item.delete()
            messages.success(request, "Item removed from your cart.")
        else:
            messages.error(request, "Item not found in your cart.")
    else:
        # For guests, update the cart stored in the session
        cart = request.session.get('cart', [])
        cart = [item for item in cart if item['product_variant_id'] != str(product_variant.uid)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from your session cart.")

    return redirect('cart')
    