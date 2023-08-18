from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.views import APIView

# Create your views here.
# from rest_framework import generics
from .models import Feedback, Cart, CartItem, Order, OrderItem, DeliveryStatus
from we.models import Product, Rating

from accounts.permissions import *
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        user = self.request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
        
        cart_items = CartItem.objects.filter(cart = cart)

        # Calculate total price of all cart items
        total_price = sum(item.product.price * item.amount for item in cart_items)
        
        # Add total_price to each cart item object
        for item in cart_items:
            item.total_price = item.product.price * item.amount

        return cart_items

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        amount = int(request.data.get('amount', 1))  # Default to 1 if not provided
        if amount < 1:
            amount = 1  # Ensure a minimum value of 1

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
            cart_item.amount += amount
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CartManagementAPIView(APIView):
    pass
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_cart(self, user):
    #     try:
    #         cart = Cart.objects.get(user=user)
    #     except Cart.DoesNotExist:
    #         cart = Cart.objects.create(user=user)
    #     return cart

    # def get(self, request, format=None):
    #     cart = self.get_cart(request.user)
    #     cart_items = CartItem.objects.filter(cart=cart)

    #     total_price = sum(item.product.price * item.amount for item in cart_items)
        
    #     for item in cart_items:
    #         item.total_price = item.product.price * item.amount

    #     serializer = CartItemSerializer(cart_items, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     product_id = request.data.get('product_id')
    #     amount = int(request.data.get('amount', 1))

    #     if amount < 1:
    #         amount = 1

    #     try:
    #         product = Product.objects.get(pk=product_id)
    #     except Product.DoesNotExist:
    #         return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    #     cart = self.get_cart(request.user)

    #     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    #     if not created:
    #         cart_item.amount += amount
    #         cart_item.save()

    #     serializer = CartItemSerializer(cart_item)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def delete(self, request, pk, format=None):
    #     try:
    #         instance = CartItem.objects.get(pk=pk)
    #     except CartItem.DoesNotExist:
    #         return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Only allow users to view their own reviewsa
        user_type = self.request.user.user_type
        if user_type == 'customer':
            return Order.objects.filter(user=self.request.user)
        if user_type == 'marchent':
            return Order.objects.all()


class OrderItemViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class DeliveryStatusViewSet(viewsets.ModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsMerchant]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


