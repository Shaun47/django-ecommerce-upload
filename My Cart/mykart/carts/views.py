from itertools import product
from django.shortcuts import get_object_or_404, render
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
        cart_item.quantity +=  1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
        
    return redirect('cart')
        


def cart(request,total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id =  cart_ID(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectNotExist:
        pass


    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items': cart_items,
        'tax'   : tax,
        'grand_total' : grand_total
    }
    return render(request, 'store/cart.html',context )

def remove_cart(request,pk):
    cart = Cart.objects.get(cart_id = cart_ID(request))
    product = Product.objects.get(id = pk)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.quantity = cart_item.quantity - 1
    if cart_item.quantity>1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
    # return HttpResponse(cart_item.quantity)

def remove_cart_item(request,pk):
    CartItem.objects.filter(id=pk).delete()

    return redirect('cart')
   