from rest_framework import serializers
from product.models import Product

class InlineProductSerial(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'slug',]

class InlineVariantSerial(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = [
            'sku',
            'attributes',
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
        ]


class ProductSerial(serializers.ModelSerializer):
    # parent_product = InlineProductSerial(read_only=True, source='parent')
    variants = InlineVariantSerial(read_only=True, many=True)
    
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
            'visibleAttributes',
            'variantAttributes',
            
            'variants'

            # 'parent', 
            # 'parent_product',
            ]



    def create(self, validated_data):
        if validated_data.get('image', None) == None:
            validated_data['image'] = 'bb.png'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('image', None) == None:
            validated_data['image'] = instance.image
        return super().update(instance, validated_data)
    

class ProductSecondSerial(serializers.ModelSerializer):
    # parent_product = InlineProductSerial(read_only=True, source='parent')
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