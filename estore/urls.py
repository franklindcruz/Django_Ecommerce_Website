from django.urls import path
from . import views
from estore.controller import auth, cart, wishlist, checkout,order

urlpatterns = [
    path('', views.index, name='home'),
    path('categories/', views.category, name='categories'),
    path('categories/<str:slug>/', views.category_detail, name='category_detail'),
    path('categories/<str:cate_slug>/<str:prod_slug>/',
         views.product_detail, name='product_detail'),
    
    path('search_products/',views.search_products,name='search_products'),

    path('register/', auth.register, name='register'),
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),


    path('add_to_cart/', cart.add_to_cart,
         name='add_to_cart'),
    path('cart/', cart.cart_view, name='cart_view'),
    path('update_cart/', cart.update_cart, name='update_cart'),
    path('delete_cart_item/', cart.delete_cart_item, name='delete_cart_item'),


    path('wishlist/', wishlist.wishlist_view, name='wishlist_view'),
    path('add_to_wishlist/', wishlist.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wishlist_item/', wishlist.remove_wishlist_item,
         name='remove_wishlist_item'),


    path('checkout/', checkout.checkout_view, name='checkout'),
    path('place-order/', checkout.place_order, name='place_order'),
    path('proceed_to_pay/', checkout.razorpay_check, name="proceed_to_pay"),
    
    path('my_orders/', order.my_orders, name='my_orders'),
    path('order_detail/<str:tracking_id>/', order.order_detail, name='order_detail'),

]
