from django.urls import path
from . import views
from estore.controller import auth, wishlist

urlpatterns = [
    path('', views.index, name='home'),
    path('categories/', views.category, name='categories'),
    path('categories/<str:slug>/', views.category_detail, name='category_detail'),
    path('categories/<str:cate_slug>/<str:prod_slug>/',
         views.product_detail, name='product_detail'),


    path('register/', auth.register, name='register'),
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),


    path('add_to_cart/', views.add_to_cart,
         name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    
    path('update_cart/', views.update_cart, name='update_cart'),
    
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    
    path('wishlist/', wishlist.wishlist_view, name='wishlist_view'),
    path('add_to_wishlist/', wishlist.add_to_wishlist, name='add_to_wishlist'),

]
