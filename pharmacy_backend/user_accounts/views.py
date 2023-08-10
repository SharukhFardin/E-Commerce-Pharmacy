from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Address, User
from .serializers import (
    AddressSerializer, UserSerializer,
)
from rest_framework import viewsets


#-----------------------------------------------------------------------------------------------------------------
# API related Views


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer