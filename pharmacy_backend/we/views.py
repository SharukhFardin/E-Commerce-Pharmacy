from django.shortcuts import render
# from rest_framework import generics
from .models import Organization, ProductCategory, Product, OrganizationUser, Rating
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from we.permissions import *
from user_accounts.permissions import *

from .serializers import (
    OrganizationSerializer, ProductCategorySerializer,
    ProductSerializer, OrganizationUserSerializer, RatingSerializer
)
from rest_framework import viewsets


#-----------------------------------------------------------------------------------------------------------------
# API related Views

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsOwner, IsAuthenticated]


class OrganizationUserViewSet(viewsets.ModelViewSet):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsOwner, IsAuthenticated]


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer




'''
# Role based access
class OwnerView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    required_role = 'owner'  # This should match the role value in your OrganizationUser model

    def get(self, request):
        # Your view logic here
        return Response({'message': 'Owner view'})

class AdminView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    required_role = 'admin'  # This should match the role value in your OrganizationUser model

    def get(self, request):
        # Your view logic here
        return Response({'message': 'Admin view'})
'''


