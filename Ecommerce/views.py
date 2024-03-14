from imaplib import _Authenticator
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
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

def cart(request):
    carts=Cart.objects.all()
    context={'Carts':carts}
    return render(request,'Cart/cart.html')

def profile(request):
    # username="disha"
    # context={
    #     'username':username
    # }
    return render(request,'Accounts/profile.html')

def register_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
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
            role = form.cleaned_data['role']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
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
            username = user.username
            user_role = profile.role
            return render(request, 'index.html', {'username': username, 'user_role': user_role})
    else:
        user_form = UserCreationForm()
        profile_form = RegistrationForm()

    return render(request, 'Accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})
