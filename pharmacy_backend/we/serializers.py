from rest_framework import serializers
from .models import *


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationUser
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name', 'uid', 'created_at', 'updated_at', 'slug', 'is_custom', 'organization']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uid', 'name', 'price', 'description', 'stock', 'slug']


class RatingSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Rating
        fields = ['uid', 'created_at', 'rating', 'product', 'user']


    # "id": 4,
    # "uid": "5bc0e363-4f10-4936-96b2-6e398a84d1ef",
    # "created_at": "2023-08-21T09:51:38.737273Z",
    # "rating": 4,
    # "user": 5,
    # "product": 1