from accounts.views import *
from django.urls import path, include

urlpatterns = [
    path('we/users', UserList.as_view(), name='user-list'),
    path('we/users/<str:uid>', UserSpecificManagement.as_view(), name='user-detail'),
    path('user/registration', UserRegistration.as_view(), name='user-registration'),
]
