from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *


# Serializer for user models
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def validate_password(self, value: str) -> str:
        return make_password(value)


# Serializer for User Address
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


# Testing User login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)