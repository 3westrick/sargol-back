from typing import Any
from django.db import models
from attribute.models import Attribute
from value.models import Value
from category.models import Category
import os

# Create your models here.
class Product(models.Model):
    # main
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True,default=None)

    # side
    categories = models.ManyToManyField(Category, related_name="products")
    # tags = models.ManyToManyField(Tag, related_name="products")
    image = models.ImageField(null=True, blank=True)

    # general
    type= models.CharField(max_length=50, choices=[['simple','simple'],['variation', 'variation'], ['variant', 'variant']])
    backorder= models.CharField(max_length=50,default='not_allow' ,choices=[['allow','allow'],['notify', 'notify'], ['not_allow', 'not_allow']])
    regular_price= models.IntegerField(default=0)
    sale_price= models.IntegerField(default=0)
    tax_status= models.CharField(max_length=50)
    tax_class= models.CharField(max_length=50)

    # inventory
    sku= models.CharField(max_length=50)
    mpn= models.CharField(max_length=50)
    stock_management= models.BooleanField(default=False)
    stock_status= models.CharField(max_length=50, default='in_stock', choices=[['in_stock','in_stock'],['out_of_stock','out_of_stock'],['on_backorder','on_backorder']])
    sold_individually= models.BooleanField(default=False)
    quantity= models.IntegerField(blank=True, null=True)
    stock= models.IntegerField(blank=True, null=True)
    unit= models.CharField(max_length=50)

    # shipping
    weight= models.IntegerField(default=0)
    length= models.IntegerField(default=0)
    width= models.IntegerField(default=0)
    height= models.IntegerField(default=0)
    shipping_class= models.CharField(max_length=50)

    # attributes
    # attributes= models.ManyToManyField(Attribute, related_name="products")
    # selectedValues: {},
    values = models.ManyToManyField(Value, related_name="products")
    # visibleAttributes= models.ManyToManyField(Attribute, related_name="visible_products",blank=True)
    # variantAttributes= models.ManyToManyField(Attribute, related_name="variant_products",blank=True)

    parent = models.ForeignKey('self',default=None ,null=True, on_delete=models.SET_NULL, related_name="variants")
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ["stock"]

class ProductAttribute(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    variant= models.BooleanField(default=False)
    visible= models.BooleanField(default=False)


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(null=True, blank=True)
