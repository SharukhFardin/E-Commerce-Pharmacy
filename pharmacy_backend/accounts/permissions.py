from rest_framework.permissions import BasePermission


class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'marchent'


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'customer'
    
'''
if request.user.is_authenticated:
    # Perform actions for authenticated users
else:
    # Perform actions for anonymous users



class IsMerchantOrManager(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is a merchant or manager
        user = request.user
        if user.is_authenticated:
            return user.user_type in ['merchant', 'manager']
        return False

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner or a manager when accessing a specific object
        user = request.user
        if user.is_authenticated:
            if user.user_type == 'merchant':
                return True  # Merchant can access any object
            elif user.user_type == 'manager':
                return user == obj.owner or user in obj.managers.all()
        return False

'''