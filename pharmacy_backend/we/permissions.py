from rest_framework.permissions import BasePermission
from we.models import OrganizationUser
from rest_framework.exceptions import PermissionDenied


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
        else:
            raise PermissionDenied("Only authenticated organization members can view data.")

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
        else:
            raise PermissionDenied("Only authenticated organization members can view data.")

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
        else:
            raise PermissionDenied("Only authenticated organization members can view data.")

        return False
    