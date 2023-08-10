from orders_management.views import CartViewSet, CartItemViewSet, OrderItemViewSet, OrderViewSet, DeliveryStatusViewSet, FeedbackViewSet
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'delivery-statuses', DeliveryStatusViewSet)
router.register(r'feedback', FeedbackViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # ... your other urlpatterns here ...
    path('api/', include(router.urls)),
]