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
]
