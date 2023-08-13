from rest_framework.permissions import BasePermission


class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'merchant'


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'customer'