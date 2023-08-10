from user_accounts.views import UserViewSet, AddressViewSet
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-addresses', AddressViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # ... your other urlpatterns here ...
    path('api/', include(router.urls)),
]
