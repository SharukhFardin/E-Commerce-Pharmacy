from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
# from rest_framework import generics
from .models import Feedback, Cart, CartItem, Order, OrderItem, DeliveryStatus
from we.models import Product
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

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        stock = int(request.data.get('stock', 1))  # Default to 1 if not provided

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.stock += stock
            cart_item.save()

        serializer = self.get_serializer(cart_item)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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


