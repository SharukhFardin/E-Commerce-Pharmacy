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

from user_accounts.serializers import (
    AddressSerializer, UserSerializer, MerchantLoginSerializer, CustomerLoginSerializer, UserLoginSerializer
)

from we.models import Product
from we.serializers import ProductSerializer


#-----------------------------------------------------------------------------------------------------------------
# API related Views


# API view for the User model
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated, IsMerchant]

    # Condition so that only merchant users can see user list
    def get_queryset(self):
        user_type = User.user_type
        user_type = self.request.user.user_type
        if user_type == 'marchent':
            return User.onjects.all()
        


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
    



################# Maybe Individual user login is not necessary right now. #####################

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
    

'''
# Testing user login API
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(email=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
'''
        

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