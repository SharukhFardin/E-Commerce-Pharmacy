from we.views import OrganizationViewSet, OrganizationUserViewSet, ProductCategoryViewSet, ProductViewSet, RatingViewSet
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'organizations', OrganizationViewSet)
router.register(r'organization-users', OrganizationUserViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'rating', RatingViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    # ... your other urlpatterns here ...
    path('api/', include(router.urls)),
]