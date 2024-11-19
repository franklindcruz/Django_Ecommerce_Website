from django.shortcuts import render, redirect, get_object_or_404
from ..models import Product, Order,OrderItem
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'estore/orders/my_orders.html', context)

@login_required(login_url='login')
def order_detail(request,tracking_id):
    order = get_object_or_404(Order, tracking_id=tracking_id)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'estore/orders/order_detail.html', context)