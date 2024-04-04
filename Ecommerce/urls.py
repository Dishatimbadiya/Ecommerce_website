from django.contrib import admin
from django.urls import path
from . import views
from .views import register, user_logout,user_login


urlpatterns = [
    path('',views.index,name="index"),
    path('product',views.product,name="product"),
    path('cart',views.cart,name="cart"),
    path('profile',views.profile,name="profile"),
    path('register_product',views.register_product,name="register_product"),
    path('login/', user_login, name='login'), 
    path('register', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('buynow/', views.buy_now, name='buy_now'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('buy_now_from_cart/', views.buy_now_from_cart, name='buy_now_from_cart'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('view_added_products/',views.view_added_products,name='view_added_products'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increment_quantity/<int:cart_item_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:cart_item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('product/<int:product_id>/', views.view_product, name='view_product'),
    path('order/', views.order, name='order'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('search/', views.search_product, name='search_product'),

]
