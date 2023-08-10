
# Serializers :
from rest_framework import serializers
from .models import Organization, UserAddress, ProductCategory, Product, Cart, CartItem, Order, OrderItem, DeliveryStatus, User, OrganizationUser




from rest_framework import generics
from .models import Organization, UserAddress, ProductCategory, Product, Cart, CartItem, Order, OrderItem, DeliveryStatus, User, OrganizationUser
from .serializers import (
    OrganizationSerializer, UserAddressSerializer, ProductCategorySerializer,
    ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer,
    OrderItemSerializer, DeliveryStatusSerializer, UserSerializer,
    OrganizationUserSerializer
)
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

# Create your views here.
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class DeliveryStatusViewSet(viewsets.ModelViewSet):
    queryset = DeliveryStatus.objects.all()
    serializer_class = DeliveryStatusSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrganizationUserViewSet(viewsets.ModelViewSet):
    queryset = OrganizationUser.objects.all()
    serializer_class = OrganizationUserSerializer

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'user-addresses', UserAddressViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'delivery-statuses', DeliveryStatusViewSet)
router.register(r'users', UserViewSet)
router.register(r'organization-users', OrganizationUserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # ... your other urlpatterns here ...
    path('api/', include(router.urls)),
]