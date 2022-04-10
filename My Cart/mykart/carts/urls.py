from django.urls import path,include
from . import views

urlpatterns = [
    # path('', views.cart,name='cart'),
        path('add_cart/<int:pk>/',views.add_cart, name='add_cart'),
]