from multiprocessing import AuthenticationError
from django import forms
from .models import *
from .Templates import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'seller', 'image', 'discount', 'quantity', 'category', 'brand', 'rating']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    role = forms.ChoiceField(
        widget=forms.RadioSelect, 
        choices=ROLE_CHOICES, 
        initial='buyer'
    )

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'email', 'phone_number']
