from django.shortcuts import render,redirect,get_object_or_404
from orders.models import Address
from payment.models import Order,Wallet
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction

def user_profile_view(request):
    user = request.user
    return render(request,'user_profile/user_profile.html',{'user':user})

def your_addresses(request):
    user = request.user
    addresses = Address.objects.filter(user=user).order_by('-created_at')[:3]
    return render(request,'user_profile/your_addresses.html',{'addresses' : addresses})

def your_order(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    paginator = Paginator(orders, 3)  # Show 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user_profile/your_order.html', {'page_obj': page_obj})

def your_wallet(request):
    # Get the wallet for the logged-in user
    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 0})
    # Fetch wallet details
    wallet_balance = wallet.balance
    last_updated = wallet.updated_at
    created_date = wallet.created_at

    # Pass the data to the template
    context = {
        'wallet_balance': wallet_balance,
        'last_updated': last_updated,
        'created_date': created_date,
    }
    return render(request, 'user_profile/your_wallet.html', context)

def cancel_order(request, uid):
    if request.method == 'POST':
        order = get_object_or_404(Order, uid=uid)

        # Check if the order can be canceled
        if order.order_status not in ['cancelled', 'delivered']:
            try:
                with transaction.atomic():
                    # If the payment is made, refund the amount
                    if order.payment_status == 'paid':
                        # Fetch or create wallet for the user
                        wallet, _ = Wallet.objects.get_or_create(user=order.user, defaults={'balance': 0})

                        # Refund the amount
                        wallet.balance += order.final_amount
                        wallet.save()

                        # Update the payment status to refunded
                        order.payment_status = 'refunded'

                    # Cancel the order
                    order.order_status = 'cancelled'
                    order.save()

                    messages.success(request, "Order has been successfully cancelled, and the payment has been refunded.")
            except Exception as e:
                messages.error(request, f"An error occurred while processing the refund: {str(e)}")
        else:
            messages.error(request, "This order cannot be cancelled.")
    
    return redirect('your_orders')

def return_order(request, uid):
    order = get_object_or_404(Order, uid=uid)
    
    if order.order_status == 'delivered' and order.return_status == 'no_request':
        order.return_status = 'requested'  # Mark return as requested
        order.save()
        messages.success(request, "Return request submitted successfully.")
    else:
        messages.error(request, "Return request cannot be processed.")
    
    return redirect('your_orders')

def order_detail(request,uid):
    pass

