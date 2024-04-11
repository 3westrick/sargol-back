from rest_framework import serializers
from product.models import Product, Image, ProductAttribute
from adminpanel.attribute.serial import AttributeSerial, InlineValueSerial

class InlineProductSerial(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'slug',]

class ProductGallery(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'image',
        ]

class InlineVariantSerial(serializers.ModelSerializer):
    gallery = ProductGallery(read_only=True, many=True)
    class Meta:
        model= Product
        fields = [
            'id',
            'sku',
            'title',
            'slug',
            'type',
            'backorder',
            'quantity',
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


class ProductAttributeSerial(serializers.ModelSerializer):
    attribute = AttributeSerial(read_only=True)
    class Meta:
        model = ProductAttribute
        fields = [
            'attribute',
            'variant',
            'visible'
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
            'type',
            'backorder',
            'quantity',
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


class ProductSerial(serializers.ModelSerializer):
    # parent_product = InlineProductSerial(read_only=True, source='parent')
    variants = InlineVariantSerial(read_only=True, many=True)
    gallery = ProductGallery(read_only=True, many=True)
    attributes = ProductAttributeSerial(read_only=True, many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title', 
            'slug', 
            'type',
            'backorder',
            'quantity',
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
            'type',
            'backorder',
            'description', 
            'quantity',
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
    # parent_product = InlineProductSerial(read_only=True, source='parent')
    class Meta:
        model = Product
        fields = [
            'id',
            'title', 
            'slug', 
            'type',
            'backorder',
            'description', 
            'short_description', 
            'price',
            'quantity',

            'category',
            'attributes',
            'values',

            ]