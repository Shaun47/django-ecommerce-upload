from django.shortcuts import render
from django.template import Context, Template

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
    cart,rest = Cart.objects.get_or_create(cart_id = cartID)
    cart.save()
    

    



    try:
        cart_item = CartItem.objects.get(product = product, cart = cart)
        cart_item.quantity =cart_item.quantity +  1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()

    context = Context({
        'product' : 'product'
    })
    return render(request, 'store/cart.html')

 