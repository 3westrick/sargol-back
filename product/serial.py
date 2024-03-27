from rest_framework import serializers
from product.models import Product, Image, ProductAttribute
from adminpanel.attribute.serial import AttributeSerial, InlineValueSerial
import math

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
class InlineVariantSerial(serializers.ModelSerializer):
    gallery = ProductGallery(read_only=True, many=True)
    attributes = ProductAttributeSerial(read_only=True, many=True)
    values = InlineValueSerial(many=True, read_only=True)
    class Meta:
        model= Product
        fields = [
            'id',
            'sku',
            'title',
            'slug',
            'attributes',
            'values',
            'regular_price',
            'sale_price',

            'stock',

            'weight',
            'length',
            'width',
            'height',
            'shipping_class',

            'tax_class',

            'description',
            'mpn',

            'image',
            'gallery'
        ]



class VariantSerial(serializers.ModelSerializer):
    gallery = ProductGallery(read_only=True, many=True)
    attributes = ProductAttributeSerial(read_only=True, many=True)
    class Meta:
        model= Product
        fields = [
            'sku',
            'title',
            'slug',
            'attributes',
            'values',
            'regular_price',
            'sale_price',

            'stock',

            'weight',
            'length',
            'width',
            'height',
            'shipping_class',

            'tax_class',

            'description',
            'mpn',

            'image',
            'gallery',

            'parent'
        ]

class ProductSerialList(serializers.ModelSerializer):
    gallery = ProductGallery(read_only=True, many=True)
    attributes = ProductAttributeSerial(read_only=True, many=True)

    range = serializers.SerializerMethodField('get_range', read_only=True)

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
            'range'

            ]

    def get_range(self, obj):
        variants = obj.variants.all()
        if len(variants) == 0:return obj.regular_price
        min_price = math.inf
        max_price = -math.inf
        for variant in variants:
            min_price = min(min_price, variant.regular_price)
            max_price = max(max_price, variant.regular_price)
        return f"{min_price} - {max_price}"



class ProductSerial(serializers.ModelSerializer):
    # parent_product = InlineProductSerial(read_only=True, source='parent')
    variants = InlineVariantSerial(read_only=True, many=True)
    gallery = ProductGallery(read_only=True, many=True)
    attributes = ProductAttributeSerial(read_only=True, many=True)

    range = serializers.SerializerMethodField('get_range', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title', 
            'slug', 
            'description', 
            'short_description', 

            'categories',
            'image',

            'regular_price',
            'sale_price',
            'tax_status',
            'tax_class',

            'sku',
            'mpn',
            'stock_management',
            'stock_status',
            'sold_individually',
            'stock',
            'unit',

            'weight',
            'length',
            'width',
            'height',
            'shipping_class',

            'attributes',
            'values',
            
            'variants',

            'gallery',

            'range'

            ]

    def get_range(self, obj):
        variants = obj.variants.all()
        if len(variants) == 0:return obj.regular_price
        min_price = math.inf
        max_price = -math.inf
        for variant in variants:
            min_price = min(min_price, variant.regular_price)
            max_price = max(max_price, variant.regular_price)
        return f"{min_price} - {max_price}"


class ProductSingleSerial(serializers.ModelSerializer):
    variants = InlineVariantSerial(read_only=True, many=True)
    gallery = ProductGallery(read_only=True, many=True)
    attributes = ProductAttributeSerial(read_only=True, many=True)
    values = InlineValueSerial(read_only=True, many=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'title', 
            'slug', 
            'description', 
            'short_description', 

            'categories',
            'image',

            'regular_price',
            'sale_price',
            'tax_status',
            'tax_class',

            'sku',
            'mpn',
            'stock_management',
            'stock_status',
            'sold_individually',
            'stock',
            'unit',

            'weight',
            'length',
            'width',
            'height',
            'shipping_class',

            'attributes',
            'values',
            
            'variants',

            'gallery'

            ]
    

class ProductSecondSerial(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title', 
            'slug', 
            'description', 
            'short_description', 
            'price',
            'quantity',

            'category',
            'attributes',
            'values',

            ]