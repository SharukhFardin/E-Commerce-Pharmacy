from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from autoslug import AutoSlugField


# All the models related to User Accounts will be here.


class UserManager(BaseUserManager):
    # Manager class for users

    def create_user(self, email, password=None, **extra_fields):
        # Method for creating user
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password): #autoslugfield
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


# Custom User Model for the system
class User(AbstractBaseUser, PermissionsMixin):
    "Users in the system"
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    slug = AutoSlugField(unique=True, populate_from='name')

    # organization_user = models.ForeignKey('OrganizationUser', on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    # address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    
    user_type = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)


    ROLE_CHOICES = (
        ('marchent', 'Marchent'),
        ('customer', 'Customer')
    )

    user_type = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
   
    objects = UserManager()

    USERNAME_FIELD = 'email'


    # REQUIRED_FIELDS=['first_name', 'last_name', 'username']


# Address table to hold addresses of an User. An user can have multiple address
class Address(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()


