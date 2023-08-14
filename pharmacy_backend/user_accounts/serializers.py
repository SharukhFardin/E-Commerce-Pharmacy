from rest_framework import serializers
from .models import *


# Serializer for user models
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Serializer for User Address
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


# Serializer for Merchant login
class MerchantLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# Serializer for customer login
class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# Testing User login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)