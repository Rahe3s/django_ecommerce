from django.shortcuts import render,redirect
from product.forms import CategoryForm,ProductsForm,ProductImageFormSet
from product.models import Category,products,productImages
from accounts.models import User_Details
from django.urls import reverse

def admin_dashboard(request):

    return render(request,'dashboard/dashboard.html')


def user_management_view(request):
    users = User_Details.objects.all()  
    return render(request, 'dashboard/user_management.html',{'users': users}) 

def category_management_view(request):
    categories = Category.objects.all()  
    return render(request, 'dashboard/category_management.html',{'categories': categories})

def product_management_view(request):
    products_list = products.objects.prefetch_related('product_images').all()
    return render(request, 'dashboard/product_management.html', {'products_list': products_list})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Saves the form data to the Category model
            return redirect('category_management')  # Redirect after saving
    else:
        form = CategoryForm()

    return render(request, 'dashboard/add_category.html', {'form': form})

def add_product(request):
    if request.method == 'POST':
        product_form = ProductsForm(request.POST)
        image_formset = ProductImageFormSet(request.POST, request.FILES, queryset=productImages.objects.none())
        if product_form.is_valid() and image_formset.is_valid():

            product =product_form.save()
            
            for form in image_formset.cleaned_data:
                if form:
                    image = form['image']
                    product_image = productImages(product = product, image = image)
                    product_image.save()

            return redirect('product_management') 
    else:
        product_form = ProductsForm()
        image_formset = ProductImageFormSet(queryset=productImages.objects.none())
        
    return render(request, 'dashboard/add_product.html', {'product_form':product_form, 'image_formset':image_formset})

    

