from django.contrib import admin
from we.models import *


# Register your models here.
admin.site.register(Organization)
admin.site.register(OrganizationUser)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Rating)