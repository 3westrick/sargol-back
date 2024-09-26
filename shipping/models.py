from typing import Iterable
from django.db import models
from base.models import Region
from rest_framework.exceptions import ValidationError

# Create your models here.
class Shipping(models.Model):
    title = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Zone(models.Model):
    name = models.CharField(max_length=50)
    regions = models.ManyToManyField(Region, blank=True)
    # Bt*
    wildcard = models.TextField(max_length=255, null=True, blank=True)

    def valid_country(self, country):
        for c in self.regions.all():
            if c.code == country:
                return True
        return False
    
    def valid_zip(self, postcode):
        if '*' in self.wildcard:
            wildcard = self.wildcard.split('*')[0]
            i = 0
            while i < len(wildcard) and i < len(postcode):
                if wildcard[i] != postcode[i]:
                    return False
                i+=1
            return True
        return postcode == self.wildcard

    def __str__(self) -> str:
        return self.name

class Method(models.Model):
    zone = models.ForeignKey(Zone, null=True, on_delete=models.CASCADE, related_name='methods')
    type = models.CharField(max_length=30, choices=(('free_shipping','free_shipping'), ('flat_rate','flat_rate'), ('local_pickup','local_pickup'), ))
    name = models.CharField(max_length=50)
    
    # free shipping
    free_shipping_requirements = models.CharField(max_length=50,null=True, blank=True,
                                             choices=(
                                                 ('none', 'none'),
                                                 ('coupon', 'coupon'),
                                                 ('minimum', 'minimum'),
                                                 ('minimum_or_coupon', 'minimum_or_coupon'),
                                                 ('minimum_and_coupon', 'minimum_and_coupon'),
                                             ))
    minimum_order_amount = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)

    # flate rate
    flate_rate_cost = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    flate_rate_qty = models.BooleanField(default=False)

    # local pickup
    local_pickup_cost = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    local_pickup_qty = models.BooleanField(default=False)

    taxable = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)

    def get_price(self):
        if self.type == 'free_shipping':
            return self.minimum_order_amount
        elif self.type == 'flat_rate':
            return self.flate_rate_cost
        elif self.type == 'local_pickup':
            return self.local_pickup_cost
        else:
            raise ValidationError("Sth went wrong: Shipping models.py: get_price")

    def valid_coupons(self, coupons):
        for coupon in coupons:
            if coupon.free_shipping:
                return True
        return False
    
    def valid_minimum(self,basket, auth):
        if auth:
            return basket.final_price >= self.minimum_order_amount
        return float(basket['final_price']) >= self.minimum_order_amount
    
    def free_shipping(self, basket, auth):
        print(self.free_shipping_requirements)
        if self.free_shipping_requirements == 'none':
            return True
        
        elif self.free_shipping_requirements == 'coupon':
            if auth:
                return self.valid_coupons(basket.coupons.all())
            return self.valid_coupons(basket['coupons'])
            
        elif self.free_shipping_requirements == 'minimum':
            return self.valid_minimum(basket, auth)
        
        elif self.free_shipping_requirements == 'minimum_or_coupon':
            if auth:
                return self.valid_coupons(basket.coupons.all()) or self.valid_minimum(basket)
            return self.valid_coupons(basket['coupons']) or self.valid_minimum(basket, auth)
        
        elif self.free_shipping_requirements == 'minimum_and_coupon':
            if auth:
                return self.valid_coupons(basket.coupons.all()) and self.valid_minimum(basket)
            return self.valid_coupons(basket['coupons']) and self.valid_minimum(basket, auth)
        
        return False

    def flat_rate(self, basket, auth):
        cost = 0
        items = basket.items.all() if auth else basket['items']
        for c in self.classes.all():
            for item in items:
                if item.product.shipping_class == c.shipping_class: 
                    cost += (c.cost * item.quantity) if c.cost_qty else c.cost
                else:
                    cost += (self.flate_rate_cost * item.quantity) if self.flate_rate_qty else self.flate_rate_cost
        return cost      
                    
                
    
    def local_pickup(self, basket, auth):
        cost = 0
        items = basket.items.all() if auth else basket['items']
        for item in items:
            cost += (self.local_pickup_cost * item.quantity) if self.local_pickup_qty else self.local_pickup_cost
        return cost
    
    def check_products(self, basket, auth):
        if self.type == 'free_shipping':
            return self.free_shipping(basket, auth)
        elif self.type == 'flat_rate':
            return self.flat_rate(basket, auth)
        elif self.type == 'local_pickup':
            return self.local_pickup(basket, auth)
        else:
            raise ValidationError("Sth went wrong: Shipping models.py: check_product")
        
    def __str__(self) -> str:
        return f"{self.type} | {self.get_price()}"

# flate rate
class ShippingMethod(models.Model):
    shipping_class = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    shipping_method = models.ForeignKey(Method, on_delete=models.CASCADE,related_name='classes')
    cost = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    cost_qty = models.BooleanField(default=False)

