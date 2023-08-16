from django.db import models
from we.models import Organization, Product, AbstractBaseModel
from user_accounts.models import User
from we.models import Product, Organization
#from autoslug import AutoSlugField
import uuid


# Order model for managing orders
class Order(AbstractBaseModel):
    name = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    #cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


# Models to define the items in an Order
class OrderItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


# Model for storing user feedbacks on products or orders
class Feedback(AbstractBaseModel):
    Order = models.OneToOneField(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    feedback = models.TextField()


# Cart Model for users
class Cart(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    #uid = AutoSlugField(unique=True, populate_from='user__username')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #uid = AutoSlugField(unique=True, populate_from='user__username')
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# CartItem model
class CartItem(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)


# This model will store delivary status 
class DeliveryStatus(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
        ('COMPLETED', 'Completed'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.order} - {self.status}"