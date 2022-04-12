from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.cart,name='cart'),
    path('add_cart/<int:pk>/',views.add_cart, name='add_cart'),
    path('remove_cart/<int:pk>/',views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:pk>/',views.remove_cart_item, name='remove_cart_item'),
]