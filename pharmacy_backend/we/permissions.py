from rest_framework.permissions import BasePermission
from we.models import OrganizationUser

# IsOwner, IsAdmins, IsManager, IsStaff, IsCustomer type of permissions

            
# There are problems in this class
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        
        try:
            organizationuser = OrganizationUser.objects.get(user=user)
            owner_role = organizationuser.role
        except OrganizationUser.DoesNotExist:
            return False

        if owner_role == 'owner':
            return True

        return False


class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        
        try:
            organizationuser = OrganizationUser.objects.get(user=user)
            owner_role = organizationuser.role
        except OrganizationUser.DoesNotExist:
            return False

        if owner_role == 'manager':
            return True

        return False
    

class IsOwnerOrManager(BasePermission):
    def has_permission(self, request, view):

        user = request.user
        
        try:
            organizationuser = OrganizationUser.objects.get(user=user)
            owner_role = organizationuser.role
        except OrganizationUser.DoesNotExist:
            return False

        if owner_role == 'owner' or 'manager':
            return True

        return False
    

