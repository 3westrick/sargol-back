from order.models import Order, Item, Basket
from product.models import Product, Image, ProductAttribute
from attribute.models import Attribute
from value.models import Value
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from base.models import User
from coupon.serial import CouponSerial
from option.models import Option

class InlineValueSerial(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ['id','title', 'slug', 'image','color']

class AttributeSerial(serializers.ModelSerializer):
    values = InlineValueSerial(many=True, read_only=True)
    class Meta:
        model = Attribute
        fields = ['id', 'title', 'slug', 'type', 'values']

class ItemSerial(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity', 'created_at', 'edited_at']

    def update(self, instance, validated_data):
        if instance.basket.user != self.context.get('request').user:
            raise ValidationError("Not Authorised")
        return super().update(instance, validated_data)

class ItemSerialCreate(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity', 'created_at', 'edited_at']

    def update(self, instance, validated_data):
        if instance.user != self.context.get('request').user:
            raise ValidationError("Not Authorised")
        return super().update(instance, validated_data)
 
class ProductGallery(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'image',
        ]

class ProductAttributeSerial(serializers.ModelSerializer):
    attribute = AttributeSerial(read_only=True)
    class Meta:
        model = ProductAttribute
        fields = [
            'attribute',
            'variant',
            'visible'
        ]

class ProductInlineSerial(serializers.ModelSerializer):
    gallery = ProductGallery(read_only=True, many=True)
    attributes = ProductAttributeSerial(read_only=True, many=True)
    tax_price = serializers.SerializerMethodField(read_only=True)
    class Meta: 
        model = Product
        fields = [
            'id',
            'title', 
            'slug',
            'image',

            'regular_price',
            'sale_price',
            'stock_status',
            'stock',

            'attributes',
            'values',
            
            'gallery',

            'sku',
            'mpn',
            'tax_price'
        ]
    def get_tax_price(self, product):
        if Option.objects.get(title = 'display_prices_during_basket_and_checkout').value == 'include':
            price = product.get_price()
            request = self.context.get('request')
            user = request.user
            if user.is_authenticated:
                print(user.country)
                print(user.state)
                print(user.address)
                print(user.postcode)
                print(user.phone)
            else:
                print("Unauth")
            tax = product.tax_class
            print(tax.rates.all())
        return None

class ItemListSerial(serializers.ModelSerializer):
    product = ProductInlineSerial(read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity', 'created_at', 'edited_at']

class BasketSerial(serializers.ModelSerializer):
    items = ItemListSerial(many=True)
    coupons = CouponSerial(many=True)
    class Meta:
        model = Basket
        fields = ['user', 'items', 'final_price', 'coupons', 'discounted_price']

class OrderSerial(serializers.ModelSerializer):
    items = ItemListSerial(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'status', 'items',]



class UserTestSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'country',
            'city',
            'address',
            'post_code',
            # 'email',
            ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': True},
            'country': {'required': True},
            'city': {'required': True},
            'address': {'required': True},
            'post_code': {'required': True},

        } 