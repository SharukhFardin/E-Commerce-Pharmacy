from we.views import OrganizationViewSet, OrganizationUserViewSet, ProductCategoryViewSet, ProductViewSet, RatingViewSet, OrganizationInventoryViewSet
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'organizations', OrganizationViewSet)
router.register(r'organization-users', OrganizationUserViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
#router.register(r'products', ProductViewSet, basename='product')
router.register(r'rating', RatingViewSet)
router.register(r'inventory', OrganizationInventoryViewSet, basename='organization-inventory')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/products/', ProductViewSet.as_view({'get': 'list'}), name='product-detail'),
    path('api/products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve_by_id'}), name='product-detail-id'),
    path('api/products/<slug:slug>/', ProductViewSet.as_view({'get': 'retrieve_by_slug'}), name='product-detail-slug'),

]

# path('api/products/<str:uid>/', ProductViewSet.as_view({'get': 'retrieve'}), name='customer-product-access'),