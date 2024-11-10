# context_processors.py
from .models import Cart,Wishlist

def cart_items_count(request):
    if request.user.is_authenticated:
        return {'cart_items_count': Cart.objects.filter(user=request.user).count()}
    return {'cart_items_count': 0}

def wishlist_items_count(request):
    if request.user.is_authenticated:
        return {'wishlist_items_count': Wishlist.objects.filter(user=request.user).count()}
    return {'wishlist_items_count': 0}