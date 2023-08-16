from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from user_accounts.permissions import *
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

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
    

        #return CartItem.objects.all()

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


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# Api View for managing order
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsMerchant]

    def get_queryset(self):
        user = self.request.user
        #return CartItem.objects.filter(cart__user=user)

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise PermissionDenied("No Cart exists for placing order")
        
        order = Order.objects.filter(id=cart.order.id)

        order_items = OrderItem.objects.filter(order=order)

        product = order_items.product
        product_price = product.price

        total_price = order_items.aggregate(total_price=sum('product__price'))['total_price']

        response_data = {
            'cart_items': order_items,
            'total_price': total_price if total_price is not None else 0.0
        }

        return response_data

        #return order_items.objects.all()
    
        
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise PermissionDenied("No Cart exists for placing an order")
        
        if not cart.order:
            order = Order.objects.create(user=user, organization=cart.user.organization)
            
            cart_items = cart.cartitem_set.all()
            for cart_item in cart_items:
                OrderItem.objects.create(order=order, product=cart_item.product) #, quantity=cart_item.stock
            
            cart_items.delete()  # Remove cart items after creating order
            cart.order = order
            cart.save()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response("An order is already associated with the cart.", status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['delete'])
    def destroy_order(self, request):
        user = self.request.user

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise PermissionDenied("No Cart exists for placing an order")
        
        if cart.order:
            order = cart.order
            order.delete()
            cart.order = None
            cart.save()

            return Response("Order deleted successfully.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("No order associated with the cart.", status=status.HTTP_400_BAD_REQUEST)



class DeliveryStatusViewSet(viewsets.ModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsMerchant]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


