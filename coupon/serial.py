from rest_framework import serializers
from coupon.models import Coupon
from adminpanel.product.serial import ProductSerial
from adminpanel.category.serial import CategorySerial
from adminpanel.user.serial import UserSerial
from datetime import date

class CouponSerial(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField(read_only=True)
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
            'is_expired',

            'minimum',
            'maximum',
            'individual_use',
            'exclude_sale_items',

            'products',
            'exclude_products',

            'categories',
            'exclude_categories',

            'allowed_users',

            'usage_limit',
            'item_limit',
            'user_limit',
        ]
        
    def get_is_expired(self, obj):
        return obj.expired_at < date.today()

class CouponSingleSerial(CouponSerial):
    products = ProductSerial(read_only=True, many=True)
    exclude_products = ProductSerial(read_only=True, many=True)
    categories = CategorySerial(read_only=True, many=True)
    exclude_categories = CategorySerial(read_only=True, many=True)
    allowed_users = UserSerial(read_only=True, many=True)