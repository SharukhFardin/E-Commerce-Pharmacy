from django.shortcuts import render
# from rest_framework import generics
from .models import Organization, ProductCategory, Product, OrganizationUser, Rating
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


class OrganizationUserViewSet(viewsets.ModelViewSet):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


