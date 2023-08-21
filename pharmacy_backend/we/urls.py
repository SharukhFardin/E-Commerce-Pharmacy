from we.views import *
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

urlpatterns = [
    path('we/organization-users/', OrganizationUserList.as_view(), name='organizationuser-list'),
    path('we/organization-users/<str:uid>', OrganizationUserDetail.as_view(), name='organizationuser-detail'),

    path('we/products/categories', ProductCategoryList.as_view(), name='product-category-list'),

    path('we/products', GetOrCreateProductsMerchant.as_view(), name='get-or-create-product'),
    path('we/products/<str:uid>', GetOrUpdateProductDetailMerchant.as_view(), name='get-or-update-detail-merchant'),

    path('me/products', GetProductsListCustomer.as_view(), name='view-product-customer'),
    path('me/products/<str:slug>', GetproductDetailCustomer.as_view(), name='product-detail-customer'),

    # path('we/stock', OrganizationSpecificStockView.as_view(), name='organization-stock'),
    path('me/product/rating', RatingAPIView.as_view(), name='rate-products'),
    path('we/products/<uuid:product_uid>/ratings/', ProductRatingsList.as_view(), name='product-ratings'),

]