from rest_framework import serializers
from order.models import Order, OrderItem
from adminpanel.product.serial import ProductSerial
from adminpanel.category.serial import CategorySerial
from adminpanel.user.serial import UserSerial
from coupon.models import Coupon


class CouponSerial(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id',
            'title',
            'description',
            'type',
            'amount',
            'free_shipping',
            'expired_at',
        ]


class OrderSerial(serializers.ModelSerializer):
    coupons = CouponSerial(read_only=True, many=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'country',
            'city',
            'address',
            'post_code',
            'ip',
            'phone',
            'name',
            'email',
            'status',
            'price',
            'created_at',

            'coupons',
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