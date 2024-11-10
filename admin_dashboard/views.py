from django.shortcuts import render,redirect,get_object_or_404
from product.forms import CategoryForm,ProductsForm,ProductImageFormSet,ProductVariantForm,ProductImageUpdateFormSet
from product.models import Category,products,productImages,ProductVariant
from accounts.models import User_Details
from orders.models import Coupons
from orders.forms import CouponForm
from django.core.paginator import Paginator

def admin_dashboard(request):

    return render(request,'dashboard/dashboard.html')


def user_management_view(request):
    users = User_Details.objects.all()  
    return render(request, 'dashboard/user_management.html',{'users': users}) 

def category_management_view(request):
    categories = Category.objects.all()  
    return render(request, 'dashboard/category_management.html',{'categories': categories})

def product_management_view(request):
  
    products_list = products.objects.all()
    product_variants = ProductVariant.objects.all()


    product_paginator = Paginator(products_list, 5)
    product_page_number = request.GET.get('product_page')
    product_page_obj = product_paginator.get_page(product_page_number)


    variant_paginator = Paginator(product_variants, 5)
    variant_page_number = request.GET.get('variant_page')
    variant_page_obj = variant_paginator.get_page(variant_page_number)

    context = {
        'product_page_obj': product_page_obj,
        'variant_page_obj': variant_page_obj,
    }

    return render(request, 'dashboard/product_management.html', context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('category_management')  
    else:
        form = CategoryForm()

    return render(request, 'dashboard/add_category.html', {'form': form})

def update_category(request, uid):
    category = get_object_or_404(Category, uid=uid)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_management')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'dashboard/update_category.html', {'form': form, 'category': category})

def delete_category(request, uid):
    category = get_object_or_404(Category, uid=uid)
    if request.method == 'POST':
        category.delete()
        return redirect('category_management')
    
    return render(request, 'dashboard/delete_category.html', {'category': category})

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

def delete_product(request, uid):
    product = get_object_or_404(products, uid=uid)
    product.delete()
    return redirect('product_management')

def update_product(request, uid):
    
    product = get_object_or_404(products, uid=uid)
    if request.method == 'POST':
        product_form = ProductsForm(request.POST, request.FILES, instance=product)
        image_formset = ProductImageUpdateFormSet(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('product_management')
    else:
        product_form = ProductsForm(instance=product)
        image_formset = ProductImageUpdateFormSet(instance=product)
    return render(request, 'dashboard/update_product.html',
                   {'product_form': product_form,
                    'image_formset' : image_formset ,
                    'product': product})


def add_product_variant(request):
    if request.method == 'POST':
        product_variant_form = ProductVariantForm(request.POST)
        if product_variant_form.is_valid():
            product_variant_form.save()
            return redirect('product_management')  # Redirect to the variant management page
    else:
        product_variant_form = ProductVariantForm()
    return render(request, 'dashboard/add_product_variant.html', {'product_variant_form': product_variant_form})   

def delete_product_variant(request, uid):
    variant = get_object_or_404(ProductVariant, uid=uid)
    variant.delete()
    return redirect('product_management')

def update_product_variant(request, uid):
    variant = get_object_or_404(ProductVariant, uid=uid)
    if request.method == 'POST':
        form = ProductVariantForm(request.POST, instance=variant)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductVariantForm(instance=variant)
    return render(request, 'dashboard/update_product_variant.html', {'product_variant_form': form, 'variant': variant})

def banner_coupon_view(request):
    coupons = Coupons.objects.all()
    return render(request,'dashboard/banner_coupon.html' ,{'coupons':coupons })

def add_coupon(request):
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            coupon_form.save()
            return redirect('banner_coupon')  # Redirect to the variant management page
    else:
        coupon_form = CouponForm()
    return render(request, 'dashboard/add_coupon.html', {'coupon_form': coupon_form})   


def update_coupon(request, uid):
    coupon = get_object_or_404(Coupons, uid=uid)
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST, instance=coupon)
        if coupon_form.is_valid():
            coupon_form.save()
            return redirect('banner_coupon')
    else:
        coupon_form = CouponForm(instance=coupon)
    
    return render(request, 'dashboard/update_coupon.html', {'coupon_form': coupon_form, 'coupon': coupon})


def delete_coupon(request, uid):
    coupon = get_object_or_404(Coupons, uid=uid)
    coupon.delete()
    return redirect('banner_coupon')