from django.db import models
import uuid
from user_accounts.models import User
from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator

# Here we define the models related to organization and inventory


# Base Abstract model from where all other models in this module will be inherited.
class AbstractBaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from='name')

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)  # Replace 'name' with the field you want to use for representation


# Organization Model. Pharmacy is a organization in case of this system.
class Organization(AbstractBaseModel):
    name = models.CharField(max_length=100)
    CEO_name = models.CharField(max_length=100)


# Model to hold relavant data to every organization User. It is a inbetween model between organization & User
class OrganizationUser(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)


# Our system can have multiple type of products. This model will store those catagory data.
class ProductCategory(AbstractBaseModel):
    name = models.CharField(max_length=255)
    is_custom = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


# Model for products. Medicines in our systems case
class Product(AbstractBaseModel):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()


# Model for storing user ratings on products
class Rating(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators = [MinValueValidator(0), MaxValueValidator(5)],
        default = 5,
        help_text="Give rating in the range of 1 to 5",
    )


