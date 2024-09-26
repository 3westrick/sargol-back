from django.db import models
from product.models import Product
from category.models import Category
from base.models import User
from rest_framework.exceptions import NotFound, ValidationError
from datetime import date
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Coupon(models.Model):

    class CouponTypes(models.TextChoices):
        FIXED_BASKET = "fixed_basket", _("fixed_basket")
        FIXED_PRODUCT = "fixed_product", _("fixed_product")
        PERCENTAGE = "percentage", _("percentage")

    title = models.TextField(max_length=50)
    description = models.TextField(blank=True, null=True)

    type = models.TextField(max_length=50, choices=CouponTypes, default=CouponTypes.PERCENTAGE)
    amount = models.DecimalField(max_digits=8,decimal_places=2, default=0,)
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

    def is_whole_basket(self):
        return self.type in {
            self.CouponTypes.PERCENTAGE,
            self.CouponTypes.FIXED_BASKET,
        }

    def already_used(self, coupons):
        if self.id in coupons:
            raise ValidationError({'detail':"Coupon already in use."})
        
    # def check_on_sale(self):
    #     if self.exclude_sale_items:
    #         if self.is_whole_basket():
    #             raise ValidationError({'detail':"You cannot apply this coupon on items on sale."}) 
        
    def check_individual_use(self,coupons_len):
        if self.individual_use and coupons_len > 0:
            raise ValidationError({'detail':"The coupon should be used individualy."}) 
    
    def is_lower_than_minimum(self ,price):
        # no limit for minumum
        if self.minimum == -1 : return
        
        if price < self.minimum:
            raise ValidationError({'detail':"The price is lower than limit."})

    def is_over_the_maximum(self,price):
        # no limit for maximum
        if self.maximum == -1 : return
        
        if price > self.maximum:
            raise ValidationError({'detail':"The price is over the limit."})
    
    def product_not_in_allowed_products(self, product):
        if self.products.count() == 0: return
        if not product in self.products.all():
            raise ValidationError({'detail': f"{product.title} can't be in list"})
    
    def product_in_excluded_products(self, product):
        if self.exclude_products.count() == 0: return
        if product in self.exclude_products.all():
            raise ValidationError({'detail':f"{product.title} can't be in list"})
    
    def categories_not_in_allowed_categories(self, product):
        if self.categories.count() == 0: return 
        categories = self.categories.all()
        for category in product.categories.all():
            if not category in categories:
                raise ValidationError({'detail': f"{product.title} can't be in list"})

    def categories_in_excluded_categories(self, product):
        if self.exclude_categories.count() == 0: return
        categories = self.categories.all()
        for category in product.categories.all():
            if category in categories:
                raise ValidationError({'detail':f"{product.title} can't be in list"})
    
    def user_not_allowed(self, user):
        if self.allowed_users.count() == 0: return
        if not user in self.allowed_users.all():
            raise ValidationError({'detail':"This user cannot use this coupon."})
    
    def is_reached_usage_limit(self):
        if self.usage_limit == -1: return
        if not self.usage_limit > 0:
            raise ValidationError({'detail': "Coupon usage has reached its limit usage."})
    
    def is_reached_item_limit(self, items_count):
        if self.item_limit == -1 : return
        if items_count > self.item_limit:
            raise ValidationError({'detail': "Number of items is more than the limit."})
    
    def is_reached_per_person_limit(self, user):
        if self.user_limit == -1: return 
        if self.user_used.filter(pk=user.id).count() > self.user_limit:
            raise ValidationError(f"User usage limit reached.")
        
    def check_date(self):
        if self.expired_at is not None and self.expired_at < date.today():
            raise ValidationError({'detail':"Coupon expired."})
        
    # def calculate_price_of_product(self, product):
