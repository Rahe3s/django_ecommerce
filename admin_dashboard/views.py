from django.shortcuts import render,redirect
from product.forms import CategoryForm
from product.models import Category

def admin_dashboard(request):
    return render(request,'dashboard/dashboard.html')


def user_management_view(request):
    
    return render(request, 'dashboard/user_management.html') 

def category_management_view(request):
    categories = Category.objects.all()
    
    return render(request, 'dashboard/category_management.html',{'categories': categories})

def product_management_view(request):
   
    return render(request, 'dashboard/product_management.html')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Saves the form data to the Category model
            return redirect('category_management')  # Redirect after saving
    else:
        form = CategoryForm()

    return render(request, 'dashboard/add_category.html', {'form': form})

