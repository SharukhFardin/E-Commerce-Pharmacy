from django.shortcuts import render
# from rest_framework import generics
from .models import Organization, ProductCategory, Product, OrganizationUser, Rating
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from we.permissions import *
from we.models import *
from user_accounts.permissions import *
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    authentication_classes = [IsAuthenticated]


# API view that will manage product management.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user:
            return Product.objects.all()
        else:
            raise PermissionDenied("User is not logged in")
        
    def perform_create(self, serializer):
        # Check if the user is a owner or manager before allowing the creation
        user_type = self.request.user.user_type

        if user_type == 'marchent':
            serializer.save()
        else:
            raise PermissionDenied("Only authenticated organization members can create users.")
        
    def perform_update(self, serializer):
        # Check if the user is a owner or manager before allowing the full update
        user_type = self.request.user.user_type

        if user_type == 'marchent':
            serializer.save()
        else:
            raise PermissionDenied("Only authenticated organization members can update data.")

    def perform_partial_update(self, serializer):
        # Check if the user is a owner or manager before allowing the partial update
        user_type = self.request.user.user_type

        if user_type == 'marchent':
            serializer.save()
        else:
            raise PermissionDenied("Only authenticated organization members can update data.")

    def perform_destroy(self, instance):
        # Check if the user is a owner or manager before allowing the deletion
        user_type = self.request.user.user_type

        if user_type == 'marchent':
            instance.delete()
        else:
            raise PermissionDenied("Only authenticated organization members can delete data.")


# API view for managing user rating
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]


class OrganizationInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsMerchant]

    def get_queryset(self):
        # Retrieve the organization from the user or any other way you have it
        authenticated_user = self.request.user
        organization_user = OrganizationUser.objects.filter(user=authenticated_user).first()

        organization = organization_user.organization  # Replace 'organization' with your actual field

        # Filter the products based on the organization
        #product_category = ProductCategory.objects.filter(organization = organization).first()
        #queryset = Product.objects.filter(category=product_category)

        queryset = Product.objects.filter(category__organization=organization)


        return queryset



