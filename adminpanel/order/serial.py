from rest_framework import serializers
from order.models import Order, OrderItem
from adminpanel.product.serial import ProductSerial
from adminpanel.category.serial import CategorySerial
from adminpanel.user.serial import UserSerial

class OrderSerial(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'price',
        ]

class OrderItemSerial(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
            'price',
            'created_at',
            'edited_at',
        ]

class OrderSingleSerial(serializers.ModelSerializer):
    items = OrderItemSerial(many=True, read_only=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'price',

            'items',
            'created_at',
            'edited_at',
        ]