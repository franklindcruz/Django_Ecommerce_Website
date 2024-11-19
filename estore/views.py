from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'estore/index.html')


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

def search_products(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    productsList= list(products)
    
    return JsonResponse(productsList, safe=False)