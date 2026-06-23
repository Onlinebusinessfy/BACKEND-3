from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate_stock(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "El stock no puede ser negativo."
            )

        return value


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate_quantity(self, value):

        if value < 1:
            raise serializers.ValidationError(
                "La cantidad debe ser mayor a cero."
            )

        return value

    def create(self, validated_data):

        product = validated_data["product"]
        quantity = validated_data["quantity"]

        if product.stock < quantity:
            raise serializers.ValidationError(
                "Stock insuficiente."
            )

        subtotal = product.price * quantity

        product.stock -= quantity
        product.save()

        validated_data["subtotal"] = subtotal

        item = super().create(validated_data)

        order = validated_data["order"]

        total = sum(
            x.subtotal
            for x in order.items.all()
        )

        order.total_amount = total
        order.save()

        return item


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = '__all__'