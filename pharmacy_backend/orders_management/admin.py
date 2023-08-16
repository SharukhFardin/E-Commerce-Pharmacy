from django.contrib import admin
from orders_management.models import *


# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(DeliveryStatus)
