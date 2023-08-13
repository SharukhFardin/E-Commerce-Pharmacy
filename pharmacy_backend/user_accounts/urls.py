from user_accounts.views import UserViewSet, AddressViewSet, MerchantLoginAPIView, CustomerLoginAPIView, MerchantView, CustomerView
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-addresses', AddressViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/merchant/login/', MerchantLoginAPIView.as_view(), name='merchant_login'),
    path('api/customer/login/', CustomerLoginAPIView.as_view(), name='customer_login'),
    path('api/merchant/dashboard/', MerchantView.as_view(), name='merchant_dashboard'),
    path('api/customer/dashboard/', CustomerView.as_view(), name='customer_dashboard'),
]
