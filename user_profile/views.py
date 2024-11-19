from django.shortcuts import render,redirect,get_object_or_404
from orders.models import Address
from payment.models import Order
from django.core.paginator import Paginator
from django.contrib import messages

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
    return render(request,'user_profile/your_wallet.html')

def cancel_order(request, order_uid):
    if request.method == 'POST':
        order = get_object_or_404(Order, uid=order_uid)
        if order.order_status not in ['cancelled', 'delivered']:
            order.order_status = 'cancelled'
            order.save()
            messages.success(request, "Order has been successfully cancelled.")
        else:
            messages.error(request, "This order cannot be cancelled.")
    
    return redirect('your_order') 

def return_order(request, uid):
    order = get_object_or_404(Order, uid=uid)
    
    if order.order_status == 'delivered' and order.return_status == 'no_request':
        order.return_status = 'requested'  # Mark return as requested
        order.save()
        messages.success(request, "Return request submitted successfully.")
    else:
        messages.error(request, "Return request cannot be processed.")
    
    return redirect('order_management')

def order_detail(request,uid):
    pass