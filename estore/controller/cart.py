from django.shortcuts import render, redirect, get_object_or_404
from ..models import Product, Cart
from django.contrib.auth.models import User
from django.http import JsonResponse


def add_to_cart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = get_object_or_404(Product, id=product_id)
            if (product_check):
                if Cart.objects.filter(product=product_check, user=request.user).exists():
                    return JsonResponse({
                        'status': 'Product already in cart',
                        'cart_items_count': Cart.objects.filter(user=request.user).count()
                    })
                else:
                    product_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= product_qty:
                        Cart.objects.create(
                            product=product_check, user=request.user, quantity=product_qty)

                        return JsonResponse({
                            'status': 'Product added to cart',
                            'cart_items_count': Cart.objects.filter(user=request.user).count()
                        })
                    else:
                        return JsonResponse({
                            'status': 'Only ' + str(product_check.quantity) + ' items available',
                            'cart_items_count': Cart.objects.filter(user=request.user).count()
                        })
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
            return JsonResponse({
                'status': 'Cart Updated',
                'cart_items_count': Cart.objects.filter(user=request.user).count()})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'Product not found in cart'}, status=404)
    return JsonResponse({'status': 'Unauthorized'}, status=401)


def delete_cart_item(request):
    if request.method == "POST" and request.user.is_authenticated:
        prod_id = int(request.POST.get('product_id'))
        try:
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.delete()
            return JsonResponse({
                'status': 'Product removed from cart',
                'cart_items_count': Cart.objects.filter(user=request.user).count()})
        except Cart.DoesNotExist:
            return JsonResponse({'status': 'Product not found in cart'}, status=404)
    return JsonResponse({'status': 'Unauthorized'}, status=401)
