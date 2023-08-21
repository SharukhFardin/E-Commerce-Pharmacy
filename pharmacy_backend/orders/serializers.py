from rest_framework import serializers
from .models import *
from we.serializers import ProductSerializer
from accounts.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('uid', 'created_at', 'updated_at', 'name', 'delivery_address')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer() # Nested Serializer
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity
    
    class Meta:
        model = CartItem
        fields = ('uid', 'product', 'quantity', 'quantity', 'total_price')


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        fields = ('uid', 'order', 'status', 'updated_at')