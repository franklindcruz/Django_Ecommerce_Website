from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from estore.models import Wishlist, Product
from django.http import JsonResponse


@login_required(login_url='login')
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist
    }
    return render(request, 'estore/wishlist.html', context)


def add_to_wishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=product_id)
            user = User.objects.get(id=request.user.id)

            if Wishlist.objects.filter(product=product_check, user=user).exists():
                return JsonResponse({
                    'status': 'Already in wishlist',
                    'wishlist_items_count': Wishlist.objects.filter(user=user).count()
                })
            else:
                wishlist = Wishlist(product=product_check, user=user)
                wishlist.save()
                return JsonResponse({
                    'status': 'Added to wishlist',
                    'wishlist_items_count': Wishlist.objects.filter(user=user).count()
                })
        else:
            return JsonResponse({'status': 'Login required'})
    else:
        return redirect('home')


def remove_wishlist_item(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            product_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=product_id)
            user = User.objects.get(id=request.user.id)

            if Wishlist.objects.filter(product=product_check, user=user).exists():
                wishlist = Wishlist.objects.filter(
                    product=product_check, user=user).first()
                wishlist.delete()
                return JsonResponse({
                    'status': 'Removed from wishlist',
                    'wishlist_items_count': Wishlist.objects.filter(user=user).count()
                })
            else:
                return JsonResponse({'status': 'Not in wishlist'})
        else:
            return JsonResponse({'status': 'Login required'})
    else:
        return redirect('home')
