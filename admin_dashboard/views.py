from django.shortcuts import render

def admin_dashboard(request):
    return render(request,'dashboard/dashboard.html')


def user_management_view(request):
    
    return render(request, 'dashboard/user_management.html')  # Full page

def category_management_view(request):
    
    return render(request, 'dashboard/category_management.html')

def product_management_view(request):
   
    return render(request, 'dashboard/product_management.html')