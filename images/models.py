from django.db import models
from product.models import Product

# Create your models here.


class Image(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    # image = models.ImageField(upload_to='images/')
    image = models.ImageField(null=True, blank=True)