from we.views import *
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# Create a router and register our viewsets with it.
router = DefaultRouter()

#router.register(r'organizations', OrganizationViewSet)

router.register(r'organization-users', OrganizationUserViewSet)
#router.register(r'product-categories', ProductCategoryViewSet)
#router.register(r'products', ProductViewSet, basename='product')
#router.register(r'rating', RatingViewSet)
#router.register(r'stock', OrganizationInventoryViewSet, basename='organization-inventory')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('we/', include(router.urls)),
    path('we/products/', GetProductList.as_view(), name='product-list'),
    path('we/product/<str:uid>', GetproductDetailMerchant.as_view(), name='product-detail-merchant'),
    path('me/products/<str:slug>', GetproductDetailCustomer.as_view(), name='product-detail-customer'),
    path('we/products/<str:uid>/', UpdateProductDetail.as_view(), name='product-update'),
    path('we/products/<str:uid>/', DeleteProduct.as_view(), name='product-delete'),
    path('we/stock', OrganizationSpecificStockView.as_view(), name='organization-stock'),
    path('me/products/rating', RatingAPIView.as_view(), name='product-rating'),

]

# path('api/products/<str:uid>/', ProductViewSet.as_view({'get': 'retrieve'}), name='customer-product-access'),