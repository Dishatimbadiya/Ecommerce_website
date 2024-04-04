from decimal import Decimal
from imaplib import _Authenticator
from pyexpat.errors import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from h11 import PRODUCT_ID
from django.db import transaction
from .models import *
from .forms import *

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        role = user_profile.role
    except UserProfile.DoesNotExist:
        role = 'buyer'
    return render(request, 'Accounts/profile.html', {'role': role})

def user_logout(request):
    logout(request)
    return redirect('index') 

def index(request):
    return render(request,'index.html')

def custom_login(request):
    return render(request,'Accounts/login.html')

@login_required
def order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'Order/order.html', {'orders': orders})

def category_products(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'Category/view_category_products.html', {'products': products})

@login_required
def place_order(request, product_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        card_number = request.POST.get('card_number')
        expiry = request.POST.get('expiry')
        cvv = request.POST.get('cvv')
        
        product = get_object_or_404(Product, id=product_id)
        cart_item = get_object_or_404(CartItem, cart=request.user.cart, product=product)
        
        # Create an order for the selected product
        order = Order.objects.create(
            name=name,
            email=email,
            address=address,
            card_number=card_number,
            expiry=expiry,
            cvv=cvv,
            user=request.user
        )
        
        # Create an OrderItem for the selected product
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=cart_item.quantity
        )
        
        # Remove the ordered item from the user's cart
        cart_item.delete()
        
        # Redirect to order detail page for the newly created order
        return redirect('order_detail', order_id=order.id)
    else:
        return render(request, 'buynow.html')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    ordered_items = OrderItem.objects.filter(order=order)
    return render(request, 'Order/order_details.html', {'order': order, 'ordered_items': ordered_items})

def product(request):
    products = Product.objects.all()
    return render(request, 'Products/product.html', {'products': products})

@login_required
def cart(request):
    try:
        user_cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        user_cart = Cart.objects.create(user=request.user)
    return render(request, 'Cart/cart.html', {'cart': user_cart})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product)
        
        if created:
            cart_item.quantity = 1
            cart_item.item_price = Decimal(str(product.price))  
        else:
            cart_item.quantity += 1 
            cart_item.item_price += Decimal(str(product.price))
        user_cart.total_price = Decimal(str(user_cart.total_price))
        user_cart.total_price += Decimal(str(product.price))
        print(user_cart.total_price)
        with transaction.atomic():
            cart_item.save()
            user_cart.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    user_cart = cart_item.cart
    user_cart.total_price -= cart_item.item_price * cart_item.quantity
    user_cart.save()
    cart_item.delete()

    return redirect('cart')


def increment_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.item_price += cart_item.product.price  # Increment the item price
    cart_item.save()
    user_cart = cart_item.cart
    user_cart.total_price += cart_item.product.price
    user_cart.save()
    return redirect('cart')

def decrement_quantity(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.item_price -= cart_item.product.price 
        cart_item.save()
    else:
        cart_item.delete()
    user_cart = cart_item.cart
    user_cart.total_price -= cart_item.product.price
    user_cart.save()
    return redirect('cart')


def buy_now(request):
    if request.method == 'POST':
        try:
            user_cart = Cart.objects.get(user=request.user)
            cart_items = user_cart.cartitem_set.all()
            context = {
                'cart': user_cart,
                'cart_items': cart_items,
            }
            return render(request, 'Products/buynow.html', context)
        except Cart.DoesNotExist:
            return render(request, 'error.html', {'message': 'Cart not found.'})
    else:
        return HttpResponseNotAllowed(['POST'])

def view_added_products(request):
    user_id = request.session.get('userid')
    if user_id is not None:
        products = Product.objects.filter(seller=user_id)
        return render(request, 'Products/view_added_products.html', {'products': products})
    else:
        return render(request, 'error.html', {'message': 'User ID not found in session.'})
    
def buy_now_from_cart(request):
    if request.method == 'POST':
        try:
            user_cart = Cart.objects.get(user=request.user)
            cart_items = user_cart.cartitem_set.all()
            context = {
                'cart': user_cart,
                'cart_items': cart_items,
            }
            return render(request, 'Products/buynow.html', context)
        except Cart.DoesNotExist:
            return render(request, 'error.html', {'message': 'Cart not found.'})

def profile(request):
    # username="disha"
    # context={
    #     'username':username
    # }
    return render(request,'Accounts/profile.html')

def thankyou(request):
    return render(request,'helper/thankyou.html')

def register_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.created_at = timezone.now()
            product.save()
            return redirect('product')
    else:
        form = ProductForm()
    return render(request, 'Products/register_product.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    request.session['user_role'] = user_profile.role
                    request.session['userid'] =user.id
                except UserProfile.DoesNotExist:
                    request.session['user_role'] = 'buyer'

                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'Accounts/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = RegistrationForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            user_role = profile.role
            request.session['user_role'] = user_role
            user_id = user.id
            request.session['userid'] = user_id            
            form = LoginForm()
            return render(request, 'Accounts/login.html', {'form': form})
    else:
        user_form = UserCreationForm()
        profile_form = RegistrationForm()

    return render(request, 'Accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})