from rest_framework import serializers
from product.models import Product, Image, ProductAttribute
from adminpanel.attribute.serial import AttributeSerial, InlineValueSerial
import math
from django.db.models import Q
from option.models import Option

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
            'type',
            'quantity',
            'stock_status',
            'stock_management',
            'backorder',
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
            'sold_individually',

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
            'type',
            'quantity',
            'stock_status',
            'stock_management',
            'backorder',
            'attributes',
            'values',
            'regular_price',
            'sale_price',
            'sold_individually',

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
    # gallery = ProductGallery(read_only=True, many=True)
    attributes = serializers.SerializerMethodField(read_only=True)

    range = serializers.SerializerMethodField('get_range', read_only=True)
    tax_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title', 
            'slug',
            'image',
            'type',
            'quantity',
            'stock_status',
            'stock_management',
            'backorder',
            'sold_individually',

            'regular_price',
            'sale_price',
            'stock_status',
            'stock',

            'attributes',
            
            'range',
            'tax_price'
            ]
    
    def get_attributes(self,obj):
        return [ attribute.attribute.id for attribute in obj.attributes.all() ]

    def get_range(self, obj):
        variants = obj.variants.all()
        if len(variants) == 0: 
            return obj.regular_price
        min_price = math.inf
        max_price = -math.inf
        for variant in variants:
            min_price = min(min_price, variant.regular_price)
            max_price = max(max_price, variant.regular_price)
        return f"{min_price} - {max_price}"

    # def get_tax_price(self, obj):
    #     if Option.objects.get(title='price_entered_with_tax').value == 'no':
    #         if Option.objects.get(title = 'display_prices_in_the_shop').value == 'include':
    #             print(obj.tax_class)
    #     return False


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
            'type',
            'quantity',
            'stock_status',
            'stock_management',
            'backorder',

            'categories',
            'image',

            'regular_price',
            'sale_price',
            'tax_status',
            'tax_class',

            'sku',
            'mpn',
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
    related = serializers.SerializerMethodField(read_only=True)
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
            'type',
            'quantity',
            'stock_status',
            'stock_management',
            'backorder',
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

            'related'

            ]
    
    def get_related(self, obj):
        attributes = []
        for pa in obj.attributes.all():
            attributes.append(pa.attribute)

        related_products = Product.objects.filter(
            Q(attributes__attribute__in=attributes) |
            Q(categories__in=obj.categories.all())
        )[:5]

        data = InlineVariantSerial(related_products,many=True).data
        return data

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
            'type',
            'stock_status',
            'stock_management',
            'backorder',
            'sold_individually',

            'category',
            'attributes',
            'values',

            ]