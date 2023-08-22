from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from orders.views import *

urlpatterns = [

    path('me/cart', CartManagementAPIView.as_view(), name='my-cart'),
    path('me/cart/<str:uid>', CartDeleteAPIView.as_view(), name='delete-my-cart'),
    path('we/orders', OrderList.as_view(), name='fetch-orders'),
    path('me/order', OrderManagementAPIView.as_view(), name='place-order'),
    path('we/order/<str:uid>/status', DeliveryStatusMerchantAPIView.as_view(), name='view-order'),
    path('me/order/<str:uid>/status', DeliveryStatusCustomerAPIView.as_view(), name='view-order'),

    path('me/order/<str:uid>/feedback', FeedbackAPIView.as_view(), name='place-order'),
    path('we/order/<str:uid>/feedbacks', FeedbackDetail.as_view(), name='get-order-feedbacks'),

]