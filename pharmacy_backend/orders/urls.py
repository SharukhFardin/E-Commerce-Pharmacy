from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from orders.views import *

urlpatterns = [

    path('me/cart', CartManagementAPIView.as_view(), name='my-cart'),
    path('me/cart/<str:uid>', CartDeleteAPIView.as_view(), name='delete-my-cart'),
    path('we/orders', OrderList.as_view(), name='fetch-orders'),
    path('me/order', OrderManagementAPIView.as_view(), name='place-order'),
    path('we/order/status', DeliveryStatusMerchantAPIView.as_view(), name='place-order'),
    path('me/order/status', DeliveryStatusCustomerAPIView.as_view(), name='place-order'),

    path('me/order/feedback', FeedbackAPIView.as_view(), name='place-order'),
    path('we/order/feedbacks', FeedbackList.as_view(), name='get-order-feedbacks'),

]