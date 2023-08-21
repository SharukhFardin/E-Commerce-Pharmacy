from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, action
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404 
from rest_framework.exceptions import ValidationError

from we.permissions import *
from we.models import *
from accounts.permissions import *
from .models import Organization, ProductCategory, Product, OrganizationUser, Rating

from .serializers import (
    ProductCategorySerializer, ProductSerializer, OrganizationUserSerializer, RatingSerializer
)
from rest_framework import viewsets


#-----------------------------------------------------------------------------------------------------------------
# API related Views


# Generics Views for Organization Users. Only Owners can create assistants -->
class OrganizationUserList(generics.ListCreateAPIView):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsOwner]


class OrganizationUserDetail(APIView):
    permission_classes = [IsOwner]

    def get_object(self, uid):
        try:
            return OrganizationUser.objects.get(uid=uid)
        except OrganizationUser.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, uid):
        organization_user = self.get_object(uid=uid)
        serializer = OrganizationUserSerializer(organization_user)
        return Response(serializer.data)

    def put(self, request, uid):
        organization_user = self.get_object(uid=uid)
        serializer = OrganizationUserSerializer(organization_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid):
        organization_user = self.get_object(uid=uid)
        organization_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -->


# Generics Views for product Catagory. Only Owner or manager can get or create product category.
class ProductCategoryList(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsOwnerOrManager]


# API's views that will manage product management:
# Retrieving product list or create new product. For Merchants
class GetOrCreateProductsMerchant(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsMerchant]

    def get(self, request):
        products = Product.objects.all()
        serialized_products = []
    
        for product in products:
            product_data = ProductSerializer(product).data
            product_data['product_category'] = product.category.name
            serialized_products.append(product_data)
        
        return Response(serialized_products)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            product_name = serializer.validated_data.get('name')
            category_name = serializer.validated_data.get('category_name')
            stock = serializer.validated_data.get('stock')
            
            existing_product = Product.objects.filter(name=product_name).first()

            if existing_product:
                existing_product.stock += stock
                existing_product.save()
                response_data = {
                    "product": ProductSerializer(existing_product).data,
                    "message": "Product stock increased"
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                category, _ = ProductCategory.objects.get_or_create(name=category_name)
                serializer.validated_data['category'] = category.id 
                serializer.validated_data['stock'] = stock  
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Retrieving product list. FOR CUSTOMERS
class GetProductsListCustomer(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsCustomer]

    def get(self, request):
        products = Product.objects.all()
        serialized_products = []
    
        for product in products:
            product_data = ProductSerializer(product).data
            product_data['product_category'] = product.category.name
            serialized_products.append(product_data)
        
        return Response(serialized_products)


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
        product_data = ProductSerializer(product).data
        product_data['product_category'] = product.category.name
        return Response(product_data)


# Retrieving Product Detail by providing product uid. {FOR ORGANIZATION USERS}
class GetOrUpdateProductDetailMerchant(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsMerchant]

    def get_object(self, uid):
        try:
            product = Product.objects.get(uid=uid)
            print("Product found:", product)
            return product
        except Product.DoesNotExist:
            print("Product not found")
            raise PermissionDenied("Product not found")

    def get(self, request, uid):
        product = self.get_object(uid)
        product_data = ProductSerializer(product).data
        product_data['product_category'] = product.category.name
        return Response(product_data)
    
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
    
    def delete(self, request, uid):
        product = self.get_object(uid)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# APIView for User Rating
class RatingAPIView(APIView):
    serializer_class = RatingSerializer
    permission_classes = [IsCustomer]

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
    

class RatingList(APIView):
    serializer_class = RatingSerializer
    permission_classes = [IsMerchant]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        ratings = Rating.objects.filter(user=user)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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



