import random
from django.shortcuts import render, redirect, HttpResponse
from ..models import Product, Cart, Order, OrderItem, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.conf import settings

@login_required(login_url='login')
def checkout_view(request):
    cart = Cart.objects.filter(user=request.user)
    for item in cart:
        if item.quantity > item.product.quantity:
            messages.error(request, f"Sorry! {item.product.name} is out of stock.")
            return redirect('cart_view')

    cart_items = Cart.objects.filter(user=request.user)
    cart_total = 0

    for item in cart_items:
        cart_total += item.product.discount_price * item.quantity
    user_profile = Profile.objects.filter(user=request.user).first()
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'user_profile': user_profile,
        'razorpay_key': settings.RAZORPAY_KEY
    }
    print(settings.RAZORPAY_KEY)
    return render(request, 'estore/checkout.html', context)


@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':

        current_user = User.objects.filter(id=request.user.id).first()
        if not current_user.first_name:
            current_user.first_name = request.POST.get('fname')
            current_user.last_name = request.POST.get('lname')
            current_user.save()

        if not Profile.objects.filter(user=request.user).exists():
            user_profile = Profile()
            user_profile.user = request.user
            user_profile.phone = request.POST.get('phone')
            user_profile.address = request.POST.get('address')
            user_profile.city = request.POST.get('city')
            user_profile.state = request.POST.get('state')
            user_profile.country = request.POST.get('country')
            user_profile.zipcode = request.POST.get('zipcode')
            user_profile.save()

        new_order = Order()
        new_order.user = request.user
        new_order.fname = request.POST.get('fname')
        new_order.lname = request.POST.get('lname')
        new_order.email = request.POST.get('email')
        new_order.phone = request.POST.get('phone')
        new_order.address = request.POST.get('address')
        new_order.city = request.POST.get('city')
        new_order.state = request.POST.get('state')
        new_order.country = request.POST.get('country')
        new_order.zipcode = request.POST.get('zipcode')

        new_order.payment_mode = request.POST.get('payment_mode')
        new_order.payment_id = request.POST.get('payment_id')

        cart_items = Cart.objects.filter(user=request.user)
        cart_total = sum(item.product.discount_price *
                         item.quantity for item in cart_items)
        new_order.total_price = cart_total
        tracking_id = 'SHOPIFY' + '-' + str(random.randint(100000, 999999))
        new_order.tracking_id = tracking_id
        new_order.save()

        # Create order items and update product stock
        for item in cart_items:
            OrderItem.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discount_price
            )
            # Update product stock after placing the order
            item.product.quantity -= item.quantity
            item.product.save()

        # Clear cart after placing the order
        Cart.objects.filter(user=request.user).delete()
        
        payment_mode = request.POST['payment_mode']
        if payment_mode == 'Paid by Razorpay':
            return JsonResponse({'tracking_id': tracking_id, 'status': 'Your order has been placed successfully!'})
        else:
            messages.success(request, 'Your order has been placed successfully!')
        return redirect('home')


@login_required(login_url='login')
def razorpay_check(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price += item.product.discount_price * item.quantity

    return JsonResponse({'total_price': total_price})
