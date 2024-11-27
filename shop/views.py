from django.shortcuts import render
from product.models import products
from django.template.loader import render_to_string
from django.http import JsonResponse
from product.models import Category

def shop(request):
    products_list = products.objects.prefetch_related('product_images').all().order_by('-created_date')
    categories = Category.objects.all()
    return render(request, 'shop/shop.html', {'products_list': products_list, 'categories': categories})



def filter_shop(request):
    search_query = request.GET.get('search', '').strip()
    category_uid = request.GET.get('category', '').strip()
    print('fetched id',category_uid)

    # Start with all products
    products_list = products.objects.prefetch_related('product_images').all()

    # Apply search filter if search query exists
    if search_query:
        products_list = products_list.filter(product_name__icontains=search_query)

    # Apply category filter if category_id is valid
    if category_uid:
        try:
            category_uid = category_uid
            products_list = products_list.filter(category_id=category_uid)
        except ValueError:
            pass  # Invalid category ID, ignore

    # Render the filtered product list
    html = render_to_string('shop/product_list.html', {'products_list': products_list})
    return JsonResponse({'html': html})