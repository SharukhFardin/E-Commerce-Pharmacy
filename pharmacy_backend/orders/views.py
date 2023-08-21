from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets

from django.shortcuts import render
from django.db import transaction

from .models import Feedback, Cart, CartItem, Order, OrderItem, DeliveryStatus
from we.models import Product
from accounts.permissions import *
from .serializers import ( CartItemSerializer, OrderItemSerializer, DeliveryStatusSerializer, OrderSerializer, FeedbackSerializer)

    
# API View for Cart Management
class CartManagementAPIView(APIView):
    permission_classes = [IsCustomer]

    def get_cart(self, user):
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
        return cart

    def get(self, request, format=None):
        try:
            cart = self.get_cart(request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            total_price = sum(item.product.price * item.quantity for item in cart_items)
            
            for item in cart_items:
                item.total_price = item.product.price * item.quantity

            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
    
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        product_name = request.data.get('product_name')
        quantity = int(request.data.get('quantity', 1))

        if quantity < 1:
            quantity = 1

        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        cart = self.get_cart(request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDeleteAPIView(APIView):
    permission_classes = [IsCustomer]

    def delete(self, request, uid, format=None):
        try:
            instance = CartItem.objects.get(uid=uid)
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# APIView for ordermanagement
class OrderManagementAPIView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request, format=None):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            return Response({"detail": "No items in the cart."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(
                name=request.user.name,
                delivery_address="Your delivery address here",
                # organization=request.user.organization,
                user=request.user
            )

            for cart_item in cart_items:
                if cart_item.quantity > cart_item.product.stock:
                    return Response({"detail": f"Product {cart_item.product.name} is out of stock."}, status=status.HTTP_400_BAD_REQUEST)
                
                order_item = OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )

                # Reduce the stock of the product
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()

                # Delete the cart item
                cart_item.delete()

            # Delete the cart
            cart.delete()

        serializer = OrderItemSerializer(order.orderitem_set.all(), many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsMerchant]


# APIview for managing delivary-status. ONLY MERCHANTS.
class DeliveryStatusMerchantAPIView(APIView):
    permission_classes = [IsMerchant]
    serializer_class = DeliveryStatusSerializer

    def get_queryset(self):
        return DeliveryStatus.objects.all()

    def get_serializer_class(self):
        return DeliveryStatusSerializer

    def get_object(self, pk):
        try:
            return DeliveryStatus.objects.get(pk=pk)
        except DeliveryStatus.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        instance = self.get_object(pk)
        if instance is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# APIview for managing delivary-status. ONLY MERCHANTS.
class DeliveryStatusCustomerAPIView(APIView):
    permission_classes = [IsMerchant]
    serializer_class = DeliveryStatusSerializer

    def get_queryset(self):
        return DeliveryStatus.objects.all()

    def get_serializer_class(self):
        return DeliveryStatusSerializer

    def get_object(self, pk):
        try:
            return DeliveryStatus.objects.get(pk=pk)
        except DeliveryStatus.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)


class FeedbackAPIView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Merchant functionality to fetch all the product feedbacks.
class FeedbackList(APIView):
    permission_classes = [IsCustomer]

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


