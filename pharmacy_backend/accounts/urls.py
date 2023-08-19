from accounts.views import *
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

urlpatterns = [
    path('we/users', UserList.as_view(), name='user-list'),
    path('we/users/<str:uid>', UserSpecificManagement.as_view(), name='user-detail'),
    path('me/registration', UserRegistration.as_view(), name='user-registration'),

]
