from django.db import models
from base.models import Region

# Create your models here.
class Tax(models.Model):
    title = models.CharField(max_length=50)

class Rate(models.Model):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, related_name='rates')
    country = models.TextField(max_length=63)
    states = models.TextField(max_length=63)
    zip_code = models.TextField(max_length=63)
    # cities = models.TextField(max_length=63)
    name = models.TextField(max_length=63)
    rate = models.DecimalField(max_digits = 5, decimal_places = 2, default=0)
    on_shipping = models.BooleanField(default=True)

    