from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Cart
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
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


def add_to_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = get_object_or_404(Product, id=product_id)
            if (product_check):
                if Cart.objects.filter(product=product_check, user=request.user).exists():
                    return JsonResponse({'status': 'Product already in cart'})
                else:
                    product_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= product_qty:
                        Cart.objects.create(
                            product=product_check, user=request.user, quantity=product_qty)
                        return JsonResponse({'status': 'Product added to cart'})
                    else:

                        return JsonResponse({'status': 'Only ' + str(product_check.quantity) + ' items available'})
            else:
                return JsonResponse({'status': 'Product not found'})
        else:
            return JsonResponse({'status': "Login to Perform this action"})

    return redirect('home')


def cart_view(request):
    cart = Cart.objects.filter(user=request.user)
    cart_total = 0
    for item in cart:
        cart_total += item.product.discount_price * item.quantity
    context = {
        'cart_items': cart,
        'cart_total': cart_total
    }
    return render(request, 'estore/cart.html', context)


def update_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        prod_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        try:
            # Fetch or raise error if product doesn't exist in cart
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.quantity = product_qty
            cart.save()
            return JsonResponse({'status': 'Cart Updated'})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'Product not found in cart'}, status=404)
    return JsonResponse({'status': 'Unauthorized'}, status=401)

def delete_cart_item(request):
    if request.method == "POST" and request.user.is_authenticated:
        prod_id = int(request.POST.get('product_id'))
        try:
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.delete()
            return JsonResponse({'status': 'Item removed from cart'})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'Product not found in cart'}, status=404)
    return JsonResponse({'status': 'Unauthorized'}, status=401)