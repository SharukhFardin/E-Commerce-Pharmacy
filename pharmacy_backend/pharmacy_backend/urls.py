from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_accounts.urls')),
    path('', include('we.urls')),
    path('', include('orders_management.urls')),
]
'''
    path('', include('we.urls')),
    path('', include('user_accounts.urls')),
    path('', include('orders_management.urls')),
'''
