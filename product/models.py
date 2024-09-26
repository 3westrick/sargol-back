from typing import Any
from django.db import models
from attribute.models import Attribute
from value.models import Value
from category.models import Category
import os
from rest_framework.exceptions import ValidationError
from tax.models import Tax
from shipping.models import Shipping

# Create your models here.
class Product(models.Model):
    # main
    title = models.CharField(max_length=50,null=True, blank=True)
    slug = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True,default=None)

    rating = models.IntegerField(default=0)

    # side
    categories = models.ManyToManyField(Category, related_name="products")
    # tags = models.ManyToManyField(Tag, related_name="products")
    image = models.ImageField(null=True, blank=True)

    # general
    type= models.CharField(max_length=50, choices=[['simple','simple'],['variation', 'variation'], ['variant', 'variant']])
    backorder= models.CharField(max_length=50,default='not_allow' ,choices=[['allow','allow'],['notify', 'notify'], ['not_allow', 'not_allow']])
    regular_price= models.DecimalField(max_digits=8,decimal_places=2, default=0)
    sale_price= models.DecimalField(max_digits=8,decimal_places=2, default=0, blank=True)
    tax_status= models.CharField(max_length=50)
    tax_class= models.ForeignKey(Tax, null=True, on_delete=models.SET_NULL)

    # inventory
    sku= models.CharField(max_length=50)
    mpn= models.CharField(max_length=50)
    stock_management= models.BooleanField(default=False)
    stock_status= models.CharField(max_length=50, default='in_stock', choices=[['in_stock','in_stock'],['out_of_stock','out_of_stock'],['on_backorder','on_backorder']])
    sold_individually= models.BooleanField(default=False)
    quantity= models.IntegerField(blank=True, null=True)
    stock= models.IntegerField(blank=True, null=True, default=0)
    unit= models.CharField(max_length=50)

    # shipping
    weight= models.IntegerField(default=0)
    length= models.IntegerField(default=0)
    width= models.IntegerField(default=0)
    height= models.IntegerField(default=0)
    shipping_class= models.ForeignKey(Shipping, null=True, on_delete=models.SET_NULL)

    # attributes
    # attributes= models.ManyToManyField(Attribute, related_name="products")
    # selectedValues: {},
    values = models.ManyToManyField(Value, related_name="products")
    # visibleAttributes= models.ManyToManyField(Attribute, related_name="visible_products",blank=True)
    # variantAttributes= models.ManyToManyField(Attribute, related_name="variant_products",blank=True)

    parent = models.ForeignKey('self',default=None ,null=True, on_delete=models.SET_NULL, related_name="variants")
    
    def __str__(self) -> str:
        return self.title
    
    def get_price(self):
        
        if self.sale_price == 0:
            return self.regular_price
        return self.sale_price
    
    def check_individually(self, quantity):
        if self.type == 'simple':
            if self.sold_individually and quantity > 1:
                raise ValidationError({'detail':f"{self.title} can only be sold 1 item per order."}) 
        elif self.type == 'variant':
            parent = self.parent
            if parent.sold_individually and quantity > 1:
                raise ValidationError({'detail':f"{self.title} can only be sold 1 item per order."}) 


    def check_stock(self, quantity):
        if self.type == 'simple':
            if self.stock_management:
                if self.quantity > 0 and  self.quantity >= quantity :
                    self.quantity = self.quantity - quantity
                    self.save()
                    return (False, False)
                else:
                    if self.backorder == 'allow':
                        return (True, False)
                    elif self.backorder == 'notify':
                        return (True, True)
                    elif self.backorder == 'not_allow':
                        raise ValidationError({'detail':f"{self.title} is not available."}) 
                        
            else:
                if self.stock_status == 'in_stock':
                    return (False, False)
                elif self.stock_status == 'out_of_stock':
                    raise ValidationError({'detail':f"{self.title} is not available."})
                elif self.stock_status == 'on_backorder':
                        return (True, True)
                
        elif self.type == 'variant':
            parent = self.parent
            if parent.stock_management:
                if parent.quantity > 0 and  parent.quantity >= quantity :
                    parent.quantity = parent.quantity - quantity
                    parent.save()
                    return (False, False)
                else:
                    if parent.backorder == 'allow':
                        return (True, False)
                    elif parent.backorder == 'notify':
                        return (True, True)
                    elif parent.backorder == 'not_allow':
                        raise ValidationError({'detail':f"{self.title} is not available."})
            else:
                if self.quantity > 0 and  self.quantity >= quantity :
                    self.quantity = self.quantity - quantity
                    self.save()
                    return (False, False)
                else:
                    if self.backorder == 'allow':
                        return (True, False)
                    elif self.backorder == 'notify':
                        return (True, True)
                    elif self.backorder == 'not_allow':
                        raise ValidationError({'detail':f"{self.title} is not available."})

    
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
