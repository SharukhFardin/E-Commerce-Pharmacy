from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, filters
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token #Test
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound

from accounts.serializers import (
    AddressSerializer, UserSerializer, UserLoginSerializer, UserRegistrationSerializer
)

from .models import Address, User
from we.permissions import IsOwnerOrManager
from we.models import OrganizationUser


# API view for the Users.


# Api View so that only owners or managers can fetch all user information or create users.
class UserList(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrManager]

    def get(self, request):
        user_type = self.request.user.user_type
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
        
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# API View so that only managers or owners can get specific information. Update or Delete users.
class UserSpecificManagement(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrManager]

    def get(self, request, uid):
        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            raise NotFound("User not found")
        
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, uid):
        user = get_object_or_404(User, uid=uid)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, uid): 
        user = get_object_or_404(User, uid=uid)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, uid):
        authenticated_user = self.request.user
        organization_user = OrganizationUser.objects.filter(user=authenticated_user).first()

        user = User.objects.get(uid=uid)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

# View for registering users to the system. Customers.
class UserRegistration(APIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Your account has been created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User login API
class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserLoginSerializer

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
    

# For retriving address list of any user.
class UserAddressList(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerOrManager]
