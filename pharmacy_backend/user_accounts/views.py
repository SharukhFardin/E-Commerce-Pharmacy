from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import Address, User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsMerchant, IsCustomer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token #Test
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied

from user_accounts.serializers import (
    AddressSerializer, UserSerializer, UserLoginSerializer
)

from we.models import Product, OrganizationUser
from we.serializers import ProductSerializer


#-----------------------------------------------------------------------------------------------------------------
# API related Views


# API view for the User Management
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # Condition so that only merchant users can see user list
    def get_queryset(self):
        user_type = self.request.user.user_type
        if user_type == 'marchent':
            return User.objects.all()
        else:
            raise PermissionDenied("Only authenticated organization members can view data.")
        
    def perform_create(self, serializer):
        # Check if the user is a owner or manager before allowing the creation
        authenticated_user = self.request.user
        organization_user = OrganizationUser.objects.filter(user=authenticated_user).first()

        if organization_user and (organization_user.role == 'owner' or organization_user.role == 'manager'):
            serializer.save()
        else:
            raise PermissionDenied("Only authenticated organization members can create users.")
        
            #return Response({"detail": "Only owners or managers can create users."}, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        # Check if the user is a owner or manager before allowing the full update
        authenticated_user = self.request.user
        organization_user = OrganizationUser.objects.filter(user=authenticated_user).first()

        if organization_user and (organization_user.role == 'owner' or organization_user.role == 'manager'):
            serializer.save()
        else:
            raise PermissionDenied("Only authenticated organization members can update data.")

    def perform_partial_update(self, serializer):
        # Check if the user is a owner or manager before allowing the partial update
        authenticated_user = self.request.user
        organization_user = OrganizationUser.objects.filter(user=authenticated_user).first()

        if organization_user and (organization_user.role == 'owner' or organization_user.role == 'manager'):
            serializer.save()
        else:
            raise PermissionDenied("Only authenticated organization members can update data.")

    def perform_destroy(self, instance):
        # Check if the user is a owner or manager before allowing the deletion
        authenticated_user = self.request.user
        organization_user = OrganizationUser.objects.filter(user=authenticated_user).first()

        if organization_user and (organization_user.role == 'owner' or organization_user.role == 'manager'):
            instance.delete()
        else:
            raise PermissionDenied("Only authenticated organization members can delete data.")



# View for the Address model
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsMerchant]
    

# View for the Marchent accessed dashboard view
class MerchantView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsMerchant]

    # Merchant specific logics
    def get(self, request):
        pass


# View for the Customer accessed dashboard view
class CustomerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]

    # Customer specific logics
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
        

# Testing user login API
class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'access_token': access_token})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)