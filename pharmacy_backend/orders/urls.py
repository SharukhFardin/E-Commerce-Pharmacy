from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from orders.views import *

# Create a router and register our viewsets with it.
router = DefaultRouter()

# router.register(r'carts', CartViewSet)
# router.register(r'cart', CartItemViewSet) # Initially was r'cart-items' . edited it.

# Need to fix order model then create views and register this order.
router.register(r'order', OrderViewSet)
router.register(r'order-items', OrderItemViewSet) # Initially was r'order-items
router.register(r'delivery-status', DeliveryStatusViewSet)
# router.register(r'feedback', FeedbackViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # ... your other urlpatterns here ...
    path('me/', include(router.urls)),
    path('me/cart', CartManagementAPIView.as_view(), name='my-cart'),
    path('me/cart/<str:uid>', CartManagementAPIView.as_view(), name='cart-item-detail'),
]