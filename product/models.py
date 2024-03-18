from django.db import models
from attribute.models import Attribute
from value.models import Value
from category.models import Category

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
    regular_price= models.IntegerField(default=0)
    sale_price= models.IntegerField(default=0)
    tax_status= models.CharField(max_length=50)
    tax_class= models.CharField(max_length=50)

    # inventory
    sku= models.CharField(max_length=50)
    mpn= models.CharField(max_length=50)
    stock_management= models.BooleanField(default=False)
    stock_status= models.CharField(max_length=50)
    sold_individually= models.BooleanField(default=False)
    stock= models.IntegerField(default=0)
    unit= models.CharField(max_length=50)

    # shipping
    weight= models.IntegerField(default=0)
    length= models.IntegerField(default=0)
    width= models.IntegerField(default=0)
    height= models.IntegerField(default=0)
    shipping_class= models.CharField(max_length=50)

    # attributes
    attributes= models.ManyToManyField(Attribute, related_name="products")
    # selectedValues: {},
    values = models.ManyToManyField(Value, related_name="products")
    visibleAttributes= models.ManyToManyField(Attribute, related_name="visible_products",blank=True)
    variantAttributes= models.ManyToManyField(Attribute, related_name="variant_products",blank=True)

    parent = models.ForeignKey('self',default=None ,null=True, on_delete=models.SET_NULL, related_name="variants")
    
    def __str__(self) -> str:
        return self.title
