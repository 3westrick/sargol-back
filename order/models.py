from django.db import models
from product.models import Product
from base.models import User
from coupon.models import Coupon
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Basket(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    final_price = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    coupons = models.ManyToManyField(Coupon, blank=True, related_name='coupons')

    def update_price(self):
        price = 0
        for item in self.items.all():
            price += item.quantity * item.product.get_price()
        self.final_price = price
        self.save()

class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items', null=True)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        BIN = "bin", _("bin")
        PROCESSING = "processing", _("processing")
        ON_HOLD = "on_hold", _("on_hold")
        COMPLETED = "completed", _("completed")
        CANCELED = "canceled", _("canceled")
        FAILED = "failed", _("failed")
        REFUNDED = "refunded", _("refunded")
        PENDING = "pending", _("pending")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)

    ip = models.CharField(max_length=50)
    
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=250)
    email = models.EmailField()

    status = models.CharField(max_length=50, choices=OrderStatus ,default=OrderStatus.PROCESSING)
    coupons = models.ManyToManyField(Coupon, related_name='orders')
    subtotal = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    shipping_price = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return self.shipping_price + self.final_price
    
    def get_discount(self):
        return self.final_price - self.discounted_price
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8,decimal_places=2, default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    backorder = models.BooleanField(default=False)
    notify = models.BooleanField(default=False)