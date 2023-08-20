from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from orders.views import *

urlpatterns = [

    path('me/cart/items', CartManagementAPIView.as_view(), name='my-cart'),
    path('me/order', OrderManagementAPIView.as_view(), name='place-order'),
    path('we/order/status', DeliveryStatusAPIView.as_view(), name='place-order'),
    path('me/order/feedback', FeedbackAPIView.as_view(), name='place-order'),

]