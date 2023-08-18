from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import permission_classes, action
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404 
from rest_framework.exceptions import ValidationError

from we.permissions import *
from we.models import *
from accounts.permissions import *
from .models import Organization, ProductCategory, Product, OrganizationUser, Rating

from .serializers import (
    OrganizationSerializer, ProductCategorySerializer,
    ProductSerializer, OrganizationUserSerializer, RatingSerializer
)
from rest_framework import viewsets


#-----------------------------------------------------------------------------------------------------------------
# API related Views


# Not Necessart I think
'''
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsOwner, IsAuthenticated]
'''


class OrganizationUserViewSet(viewsets.ModelViewSet):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsOwner, IsAuthenticated]


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    authentication_classes = [IsAuthenticated]


# API's views that will manage product management:

# Retrieving Product List
class GetProductList(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsCustomer]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


# Retrieving Product Detail by providing product uid. {FOR ORGANIZATION USERS}
class GetproductDetailMerchant(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsMerchant]

    def get_object(self, uid):
        try:
            return Product.objects.get(uid=uid)
        except Product.DoesNotExist:
            raise PermissionDenied("Product not found")

    def get(self, request, uid):
        product = self.get_object(uid)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

# Retrieving Product Detail by providing product uid. {FOR CUSTOMERS}
class GetproductDetailCustomer(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsCustomer]

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise PermissionDenied("Product not found")

    def get(self, request, slug):
        product = self.get_object(slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

# Update or partially update product detail by providing uid
class UpdateProductDetail(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsMerchant]

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise PermissionDenied("Product not found")

    def put(self, request, uid):
        product = self.get_object(uid)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uid):
        product = self.get_object(uid)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class DeleteProduct(APIView):
    permission_classes = [IsMerchant]
    serializer_class = ProductSerializer

    def delete(self, request, uid):
        product = self.get_object(uid)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


# API view for managing user rating. Used ModelViewSet. Need to use APIView
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        # Only allow users to view their own reviews
        return Rating.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.validated_data['product']
        
        # Check if the user has already rated the same product
        existing_rating = Rating.objects.filter(user=user, product=product).first()
        if existing_rating:
            raise ValidationError("You have already rated this product.")
        
        serializer.save(user=user)


# APIView for User Rating
class RatingAPIView(APIView):
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        ratings = Rating.objects.filter(user=user)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        product = request.data.get('product')

        existing_rating = Rating.objects.filter(user=user, product=product).first()
        if existing_rating:
            raise ValidationError("You have already rated this product.")

        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrganizationInventoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsMerchant]

    def get_queryset(self):
        # Retrieve the organization from the user or any other way you have it
        authenticated_user = self.request.user
        organization_user = OrganizationUser.objects.filter(user=authenticated_user).first()

        organization = organization_user.organization

        queryset = Product.objects.filter(category__organization=organization)


        return queryset


# View for loading organization specific
class OrganizationSpecificStockView(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsMerchant]

    def get(self, request, *args, **kwargs):
        authenticated_user = self.request.user
        organization_user = OrganizationUser.objects.filter(user=authenticated_user).first()

        if not organization_user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        organization = organization_user.organization
        products = Product.objects.filter(category__organization=organization)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



