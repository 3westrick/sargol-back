from django.db import models
from product.models import Product
from category.models import Category
from base.models import User
# Create your models here.

class Coupon(models.Model):
    title = models.TextField(max_length=50)
    description = models.TextField(blank=True, null=True)

    type = models.TextField(max_length=50)
    amount = models.PositiveIntegerField(default=0)
    free_shipping = models.BooleanField(default=False)
    expired_at = models.DateField()

    minimum = models.IntegerField(default=0)
    maximum = models.IntegerField(default=0)
    individual_use = models.BooleanField(default=False)
    exclude_sale_items = models.BooleanField(default=False) # if True coupon won't apply on items on sale

    products = models.ManyToManyField(Product, related_name="coupons", blank=True)
    exclude_products = models.ManyToManyField(Product, blank=True)

    categories = models.ManyToManyField(Category, related_name="coupons", blank=True)
    exclude_categories = models.ManyToManyField(Category, blank=True)

    allowed_users = models.ManyToManyField(User, related_name="coupons", blank=True)

    usage_limit = models.IntegerField(default=0,blank=True)
    item_limit = models.IntegerField(default=0,blank=True)
    user_limit = models.IntegerField(default=0,blank=True)

    user_used = models.ManyToManyField(User, related_name="coupons_used" ,blank=True)
