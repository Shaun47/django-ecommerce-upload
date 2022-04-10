from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse
from store.models import Product
from .models import Cart, CartItem

# Create your views here.
def cart_ID(request):
    cartID = request.session.session_key
    if not cartID:
        cartID = request.session.create()
    return cartID


def add_cart(request,pk):
    product = Product.objects.get(id = pk)
    cartID = cart_ID(request)
    # cart = Cart.objects.filter(cart_id= cart_ID(request))

    
 
    cart = Cart.objects.get_or_create(cart_id = cartID)
    cart.save()
    return render(request, 'store/cart.html')

