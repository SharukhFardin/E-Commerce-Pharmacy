from accounts.views import *
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from django.urls import path, include

urlpatterns = [
    path('users', GetUserList.as_view(), name='user-list'),
    path('users/<str:uid>', GetUserDetail.as_view(), name='user-detail'),
    path('users', CreateUserAccount.as_view(), name='create-account'),
    path('users/<str:uid>', UpdateUserAccount.as_view(), name='update-account'),
    path('users/<str:uid>', DeleteUserAccounts.as_view(), name='delete-account'),
]
