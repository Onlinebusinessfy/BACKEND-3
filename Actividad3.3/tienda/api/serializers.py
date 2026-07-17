from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'product', 'product_detail',
            'quantity', 'status', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']