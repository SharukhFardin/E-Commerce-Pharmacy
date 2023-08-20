from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 'marchent':
            return True
        else:
            raise PermissionDenied("Only authenticated organization members can view data.")


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 'customer':
            return True
        else:
            raise PermissionDenied("Only authenticated organization members can view data.")
    
    