from order.models import Order, Item
from product.models import Product, Image, ProductAttribute
from attribute.models import Attribute
from value.models import Value
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
        if instance.user != self.context.get('request').user:
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
            'mpn'
        ]


class ItemListSerial(serializers.ModelSerializer):
    product = ProductInlineSerial(read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity', 'created_at', 'edited_at']


class OrderSerial(serializers.ModelSerializer):
    items = ItemListSerial(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'status', 'items',]
