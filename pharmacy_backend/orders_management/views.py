from django.shortcuts import render

# Create your views here.
# from rest_framework import generics
from .models import Feedback, Cart, CartItem, Order, OrderItem, DeliveryStatus
from .serializers import (
    CartSerializer, CartItemSerializer, OrderSerializer,
    OrderItemSerializer, DeliveryStatusSerializer, FeedbackSerializer,

)
from rest_framework import viewsets


#-----------------------------------------------------------------------------------------------------------------
# API related Views


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class DeliveryStatusViewSet(viewsets.ModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer



