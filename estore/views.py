from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


# Create your views here.
def index(request):
    trending_products = Product.objects.filter(trending=True)
    context = {
        'trending_products': trending_products
    }
    return render(request, 'estore/index.html', context)


def category(request):
    
    categories = Category.objects.filter(status=1)
    context = {
        'categories': categories
    }
    return render(request, 'estore/collections.html', context)


def category_detail(request, slug):
    if (Category.objects.filter(slug=slug, status=1).exists()):
        category = Category.objects.filter(slug=slug, status=1).first()
        products = Product.objects.filter(category=category)

        context = {
            'category': category,
            'products': products
        }
        return render(request, 'estore/products/product_list.html', context)
    else:
        messages.warning(request, 'Category not found')
        return redirect('categories')


def product_detail(request, cate_slug, prod_slug):
    if (Category.objects.filter(slug=cate_slug).exists() and Product.objects.filter(slug=prod_slug).exists()):
        category = Category.objects.filter(slug=cate_slug).first()
        # This should be a single product instance
        products = Product.objects.filter(slug=prod_slug).first()
        context = {
            'category': category,
            'products': products  # Ensure this is the single product instance
        }
        return render(request, 'estore/products/product_detail.html', context)
    else:
        messages.warning(request, 'Product not found')
        return redirect('categories')

def product_list_query(request):
    try:
        # Fetch product names with available=True
        products = Product.objects.filter(available=True).values_list('name', flat=True)
        products_list = list(products)

        # Return the list of product names
        return JsonResponse(products_list, safe=False)

    except ObjectDoesNotExist:
        # Handle cases where the query fails
        return JsonResponse({'error': 'No products found'}, status=404)

    except Exception as e:
        # Log the error (optional) and return a 500 response
        print(f"Error in search_products view: {e}")
        return JsonResponse({'error': 'Something went wrong'}, status=500)
    
def search_product(request):
    if request.method == 'POST':
        searchitem = request.POST.get('product-search')
        if not searchitem:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(name__icontains=searchitem).first()
            if product:
                # Use `reverse` to generate the correct URL
                return redirect(reverse('product_detail', args=[product.category.slug, product.slug]))
            else:
                messages.info(request, 'No results found for ' + searchitem)
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))