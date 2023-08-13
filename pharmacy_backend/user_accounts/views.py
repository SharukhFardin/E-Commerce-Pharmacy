from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import Address, User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsMerchant, IsCustomer
from rest_framework_simplejwt.authentication import JWTAuthentication

from user_accounts.serializers import (
    AddressSerializer, UserSerializer, MerchantLoginSerializer, CustomerLoginSerializer
)

#-----------------------------------------------------------------------------------------------------------------
# API related Views


# API view for the User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsMerchant]


# View for the Address model
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


# View for the marchent login
class MerchantLoginAPIView(APIView):
    def post(self, request):
        serializer = MerchantLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user and user.user_type == 'merchant':
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

class MerchantView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsMerchant]

    # Merchant specific logics
    def get(self, request):
        pass


# View for the customer login   
class CustomerLoginAPIView(APIView):
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user and user.user_type == 'customer':
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

class CustomerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsCustomer]

    # Customer specific logics
    def get(self, request):
        pass