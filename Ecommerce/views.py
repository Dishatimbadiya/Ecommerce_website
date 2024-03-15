from imaplib import _Authenticator
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from h11 import PRODUCT_ID
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
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def buy_now(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'Products/buynow.html', {'products': [product]})
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required
def view_added_products(request):
    return render(request,'Products/view_added_products.html')

def buy_now_from_cart(request):
    user_cart = Cart.objects.get(user=request.user)
    cart_items = user_cart.items.all()
    return render(request, 'Products/buynow.html', {'products': cart_items})

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
            form = LoginForm()
            return render(request, 'Accounts/login.html', {'form': form})
    else:
        user_form = UserCreationForm()
        profile_form = RegistrationForm()

    return render(request, 'Accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})